# pip install pypiwin32
import win32com
from win32com.client import Dispatch
import os
ppt = win32com.client.Dispatch('PowerPoint.Application')
ppt.Visible = 1
pptSel = ppt.Presentations.Open(os.getcwd()+"\\"+'1.ppsx')
slide_count = pptSel.Slides.Count
for i in range(1,slide_count + 1):
	shape_count = pptSel.Slides(i).Shapes.Count
	for j in range(1,shape_count+1):
		if pptSel.Slides(i).Shapes(j).HasTextFrame:
			s = pptSel.Slides(i).Shapes(j).TextFrame.TextRange.Text
			print(s)