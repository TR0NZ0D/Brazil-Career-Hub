Write-Host "Checking if node js is installed on your machine"
$nodeOutput = Invoke-Expression "node -v"
if ($nodeOutput -match "[v]\d\d[.]\d\d[.]\d") {
  Write-Host "Node is installed, your version is" $nodeOutput
  
  if (Test-Path "./node_modules") {
    Write-Host "Dependencies is already installed"
  }

  else {
    Write-Host "Dependecies not found!"
    Write-Host "Installing dependencies"
    Invoke-Expression "npm install"
  }

  Invoke-Expression "npm start"
}

else {
  Write-Host "Node is not installed, please install it so you can execute the front-end project"
}
