# Masaustu ve Baslat menusune "Ders Kitabi Denetleyici" kisayolu ekler (-Kaldir ile siler).
# KURULUM.bat ve uygulama\kaldir.bat tarafindan cagrilir.
param([switch]$Kaldir)

$kok = Split-Path -Parent $PSScriptRoot
# Kisayol adindaki Turkce "i" harfi, dosya kodlamasindan etkilenmesin diye karakter koduyla yazildi
$ad = "Ders Kitab" + [char]0x0131 + " Denetleyici"
$klasorler = @([Environment]::GetFolderPath("Desktop"), [Environment]::GetFolderPath("Programs"))

foreach ($klasor in $klasorler) {
    $yol = Join-Path $klasor "$ad.lnk"
    if ($Kaldir) {
        if (Test-Path $yol) { Remove-Item $yol; Write-Host "Kaldirildi: $yol" }
        continue
    }
    $kisayol = (New-Object -ComObject WScript.Shell).CreateShortcut($yol)
    $kisayol.TargetPath = Join-Path $kok "BASLAT.bat"
    $kisayol.WorkingDirectory = $kok
    $kisayol.IconLocation = (Join-Path $PSScriptRoot "simge.ico") + ",0"
    $kisayol.Description = "Ders kitaplarinda icerik ve tutarlilik hatalarinin otomatik tespiti"
    $kisayol.Save()
    Write-Host "Kisayol olusturuldu: $yol"
}
