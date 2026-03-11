; Environment setup
; #Warn
SendMode "Input"
SetWorkingDir A_ScriptDir
#SingleInstance Force

; Configuration
SVV := "C:\Tools\SoundVolumeView\SoundVolumeView.exe"
SPOTIFY_ID := "Realtek(R) Audio\Application\Spotify"
Step := 5

; Display sound toggle GUI
soundToggleBox(Device) {
    global soundToggleGui
    if WinExist("soundToggleWin") {
        soundToggleGui.Destroy()
    }
    soundToggleGui := Gui("+ToolWindow -Caption +0x400000 +AlwaysOnTop")
    soundToggleGui.Add("Text", "x8 y8", "Sound: " Device)
    screenx := SysGet(0)
    screeny := SysGet(1)
    xpos := screenx - 275
    ypos := screeny - 100
    soundToggleGui.Show("NoActivate x" xpos " y" ypos " h30 w200")
    SetTimer(soundToggleClose, -1000)
}

soundToggleClose() {
    global soundToggleGui
    soundToggleGui.Destroy()
}

; Spotify volume control with Alt + PgUp/PgDn
ChangeSpotify(delta) {
    global SVV, SPOTIFY_ID
    Run('"' SVV '" /ChangeVolume "' SPOTIFY_ID '" ' delta, , "Hide")
    soundToggleBox("Spotify " (delta > 0 ? "+" : "") delta "%")
}

!PgUp::ChangeSpotify(Step)
!PgDn::ChangeSpotify(-Step)

; Global volume control with Alt + Arrow keys
>!Up::Send("{Volume_Up}")
>!Down::Send("{Volume_Down}")
>!Left::Send("{Media_Prev}")
>!Right::Send("{Media_Next}")
>!m::Send("{Volume_Mute}")
>!Space::Send("{Media_Play_Pause}")