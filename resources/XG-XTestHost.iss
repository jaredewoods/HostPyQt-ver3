[Setup]
AppName=XG-X Test Host
AppVersion=3.0
DefaultDirName={pf}\XG-X Test Host
DefaultGroupName=XG-X Test Host
OutputDir=.
OutputBaseFilename=XG-XTestHostInstaller

[Files]
Source: "C:\Users\bgrepair\PycharmProjects\HostPyQt-ver3\dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\bgrepair\PycharmProjects\HostPyQt-ver3\resources\macro_sequences\*"; DestDir: "{app}\macro_sequences"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\bgrepair\PycharmProjects\HostPyQt-ver3\resources\docs\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\bgrepair\PycharmProjects\HostPyQt-ver3\logs\*"; DestDir: "{app}\logs"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\XG-X Test Host"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,XG-X Test Host}"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[CustomMessages]
CreateDesktopIcon=Create a &desktop icon:

[Components]
Name: "core"; Description: "Core Files"; Types: full compact custom; Flags: fixed

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
