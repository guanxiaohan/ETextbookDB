[System.Collections.ArrayList]$Processes=@()
$Count = 0

function addProcess{
    param(
        [string]$uri
    )
    $Process = Start-Process -FilePath "powershell" -ArgumentList "-File ./process.ps1 -Uri $uri" -PassThru
    $Processes = $Processes.Add([PSCustomObject]@{renameTo="a"
                                    moveTo="a"
                                    process=$Process
                                    uri=$uri
                                    id=($global:Count + 1)})
    $global:Count += 1
}

function ShowProcesses {
    Write-Host ""
    Write-Host "Processes in Queue:"

    foreach ($p in $Processes){
        Write-Host "#$($p.id) Process: $($p.renameTo)"
        Write-Host "    - Uri: $($p.uri)"
        Write-Host ""
    }
}

function GetRename {
    param (
        $subject
    )
    $Processes[-1].renameTo = (Read-Host "Enter textbook version (RJ, SD, etc.)") + "_$subject" + "_G" + (Read-Host "Enter Grade") + "S" +`
        (Read-Host "Enter Semester(1 or 2)") + "_" + (Get-Date -Format "yyyyMMdd") + ".pdf"
}

function AddNew{
    $uri = Read-Host "Enter Uri"
    addProcess $uri

    $Folder = Read-Host "Enter Subject name (Mathematics, Politics, etc.)"
    $Processes[-1].moveTo = "./$Folder"
    GetRename $Folder

    Write-Output "Started process to download $uri."
    Write-Output "Will save to $($Processes[-1].moveTo)/$($Processes[-1].renameTo)"
}

function main{
    while ($true){
        Write-Host ""
        Write-Host "Adding new download process #$(($global:Count + 1))."
        AddNew

        $Continue = Read-Host "Do you want to add another process(a) or wait for the queue(w)?"
        if ($Continue -eq "w"){
            ShowProcesses
            while ($true) {
                Start-Sleep -Seconds 1
                foreach ($p in $Processes){
                    if ($p.process.HasExited){
                        try {
                            Write-Host "Process #$($p.id) has finished with code $($p.process.ExitCode)"
                            if ($p.process.ExitCode -eq 200){
                                Write-Host "- Finished downloading $($p.uri)"
                                Write-Host "- Cached at ./Cache_$($p.uri.Split("_")[-1].Split("/")[-1]).pdf"
                                Write-Host "- Moving to $($p.moveTo)/$($p.renameTo)"
                                Move-Item -Path "./Cache_$($p.uri.Split("_")[-1].Split("/")[-1]).pdf" -Destination "$($p.moveTo)/$($p.renameTo)"
                                Write-Host "- Moved successfully."
                            }
                            else {
                                Write-Warning "Failed to download $($p.uri)"
                            } 
                        }
                        catch {
                            Write-Warning "Error occurred while processing. $_"
                        }
                        Write-Host ""
                        $Processes = $Processes | Where-Object {$_ -ne $p}
                        ShowProcesses
                    }
                }

                if ($Processes.Count -eq 0){
                    Write-Host ""
                    Write-Host "All $global:Count processes have finished."
                    Read-Host "Press Enter to exit"
                    return
                }
            }
        }
        elseif ($Continue -eq "a"){
            continue
        }
    }   
}

main