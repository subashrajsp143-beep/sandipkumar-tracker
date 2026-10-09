param([string]$ImagePath)

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { 
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' 
}

function Await-WinRT($operation, [Type]$returnType) {
    $netTask = $asTaskGeneric.MakeGenericMethod($returnType).Invoke($null, @($operation))
    $netTask.Wait()
    return $netTask.Result
}

[Windows.Media.Ocr.OcrEngine, Windows.Foundation.UniversalApiContract, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation.UniversalApiContract, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Foundation.UniversalApiContract, ContentType = WindowsRuntime] | Out-Null

$storageFileType = [Windows.Storage.StorageFile]
$streamType = [Windows.Storage.Streams.IRandomAccessStreamWithContentType]
$decoderType = [Windows.Graphics.Imaging.BitmapDecoder]
$bitmapType = [Windows.Graphics.Imaging.SoftwareBitmap]
$ocrResultType = [Windows.Media.Ocr.OcrResult]

$file = Await-WinRT ([Windows.Storage.StorageFile]::GetFileFromPathAsync($ImagePath)) $storageFileType
$stream = Await-WinRT ($file.OpenReadAsync()) $streamType
$decoder = Await-WinRT ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) $decoderType
$bitmap = Await-WinRT ($decoder.GetSoftwareBitmapAsync()) $bitmapType

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$ocrResult = Await-WinRT ($engine.RecognizeAsync($bitmap)) $ocrResultType

foreach ($line in $ocrResult.Lines) {
    Write-Output $line.Text
}
