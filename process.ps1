param($Uri = (throw "Missing Uri."))

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"

$Smartedu_Headers = @{
    "authority"="r2-ndr-private.ykt.cbern.com.cn"
    "method"="GET"
    "path"="/edu_product/esp/assets/8f907d12-14b5-44ba-b042-0ffbc46e085b.pkg/%E4%B9%89%E5%8A%A1%E6%95%99%E8%82%B2%E6%95%99%E7%A7%91%E4%B9%A6%20%E8%AF%AD%E6%96%87%20%E5%85%AB%E5%B9%B4%E7%BA%A7%20%E4%B8%8B%E5%86%8C_1737863671828.pdf"
    "scheme"="https"
    "accept"="*/*"
    "accept-encoding"="gzip, deflate, br, zstd"
    "accept-language"="en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-GB;q=0.6,ja;q=0.5"
    "origin"="https://basic.smartedu.cn"
    "priority"="u=1, i"
    "referer"="https://basic.smartedu.cn/"
    "sec-ch-ua"="`"Not A(Brand`";v=`"8`", `"Chromium`";v=`"132`", `"Microsoft Edge`";v=`"132`""
    "sec-ch-ua-mobile"="?0"
    "sec-ch-ua-platform"="`"Windows`""
    "sec-fetch-dest"="empty"
    "sec-fetch-mode"="cors"
    "sec-fetch-site"="cross-site"
    "x-nd-auth"="MAC id=`"7F938B205F876FC3A30551F3A493138321D804F5876FD38026CB9380C9B1858D1AE4A747491FB45BAECC56EBC7CA41DBD4E4AEC647207808`",nonce=`"1738898474459:KFD4OSEA`",mac=`"Za0fV3iRMG4ene36UU8YAr7h6zeqUKzopcfl2T W1tk=`""
}

function Download{
    param (
        $Headers,
        $uri
    )
    Write-Output "Downloading $uri"

    try {
        $SaveName = $uri.Split("_")[-1].Split("/")[-1]
        $Request = Invoke-WebRequest -UseBasicParsing -Uri $uri -WebSession $session -Headers $Headers -OutFile "./Cache_$SaveName.pdf"
        Write-Host "Successfully downloaded $uri with status code $($Request.StatusCode)"
        Write-Host "Saved to Cache_$SaveName.pdf"
        exit 200
    }
    catch {
        Write-Warning "Failed to download $Uri"
        Write-Warning "Error: $_"
        Read-Host "Press Enter to continue"
        exit 404
    }
}

Download $Smartedu_Headers $Uri