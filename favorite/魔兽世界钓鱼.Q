[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=122
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=19966c6e-8224-4c20-9c9a-f746790cc999
Description=我的脚本1
Enable=0
AutoRun=0
[Repeat]
Type=1
Number=1
[SetupUI]
Type=2
QUI=
[Relative]
SetupOCXFile=
[Comment]

[Script]
//定义屏幕矩形变量
Dim x1 
Dim y1
Dim x2
Dim y2

//变量赋值
//x1 = Form1.IBx1.Text
//y1 = Form1.IBy1.Text
//x2 = Form1.IBx2.Text
//y2 = Form1.IBy2.Text\
x1 = 400
y1 = 200
x2 = 1000
y2=1000


Rem fish
//放鱼竿
KeyPress 49, 1   

//移动鼠标遍历屏幕直到找到鱼漂
intA = x1
intB = y1
i = 0
j = 0
K = 0
MoveTo intA, intB
Delay 1000

//获取鼠标形状，1053591638为鱼钩形状
shape = GetCursorShape(0)

//如果鼠标不是鱼钩形状，则右移5像素，若到达最右边，则下移30像素，从最左开始重新右移，直到遍历完指定区域，找到鱼漂后鼠标变为鱼钩状，此时退出循环
Do  While shape <> 1884068285   
    If intA + 5 > x2 Then 
            If intB + 50 > y2 Then 
                    Exit Do
            Else 
                    intA = x1
                    intB =intB + 30
            End If
            Else 
            intA = intA + 5
    End If
    MoveTo intA, intB
    shape = GetCursorShape(0)
    Delay 10
Loop

//将鼠标向上移动到鱼漂最上方恰好不变形状的位置        
Do  While shape = 1884068285
        MoveTo intA, intB
        If shape = 1884068285 Then 
                intB = intB - 1
                Delay 5
        End If        
        shape = GetCursorShape(0)
Loop

Do  While shape <> 1884068285
        MoveTo intA, intB
        If shape <> 1884068285 Then 
                intB = intB + 1
                i = i + 1
                If i > 15 Then    //15次未找到位置则认为出错，退出循环
                        Exit Do
                End If
                Delay 200
        End If
        shape = GetCursorShape(0)
Loop

//将鼠标向右移动到鱼漂最右方恰好不变形状的位置        
Do  While shape = 1884068285
        MoveTo intA, intB
        If shape = 1884068285 Then 
                intA = intA + 1
                Delay 5
        End If        
        shape = GetCursorShape(0)
Loop

//将鼠标向左移动到鱼漂右方恰好变形状的位置
Do  While shape <> 1884068285
        MoveTo intA, intB
        If shape <> 1884068285 Then 
                intA = intA - 1
                j = j + 1
                If j > 15 Then //15次未找到则认为出错，提出循环
                        Exit Do
                End If
                Delay 150
        End If        
        shape = GetCursorShape(0)
Loop

Do While 1 = 1
	sound_x = 1325
	sound_y = 494
	
	FindColor sound_x,sound_y,sound_x+13,sound_y+3,"329932",intX,intY
	If intX > 0 And intY > 0 Then 
		MoveTo intA - 2, intB + 2
        KeyDown "Shift", 1
        Delay 20
        RightDown 1
        
		Delay 150
        RightUp 1
        Delay 200
		KeyUp "Shift", 1
		
		//RightClick 1
		Goto fish
	End If
    Delay 100
    k = k + 1
    If k > 220 Then    //15次未找到位置则认为出错，退出循环
           Exit Do
         End if
Loop
