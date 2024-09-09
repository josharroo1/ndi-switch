# Create a release folder
$releaseFolderName = "NDIDecoderControl_Release"
New-Item -ItemType Directory -Force -Path $releaseFolderName

# Copy the executable
Copy-Item "dist\ndi_decoder_control.exe" -Destination $releaseFolderName

# Copy the config file
Copy-Item "config.ini" -Destination $releaseFolderName

# Create a README file
@"
NDI Decoder Control

1. Ensure both 'ndi_decoder_control.exe' and 'config.ini' are in the same folder.
2. Double-click 'ndi_decoder_control.exe' to run the application.
3. If you need to modify settings, edit the 'config.ini' file with a text editor.
"@ | Out-File -FilePath "$releaseFolderName\README.txt"

Write-Host "Package created in $releaseFolderName folder. You can distribute this folder to users."