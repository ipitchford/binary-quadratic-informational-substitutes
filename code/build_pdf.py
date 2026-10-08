#!/usr/bin/env python3
"""Typeset the mathematical manuscript with ReportLab; draw exact-formula figure.

Runtime requirements: reportlab, matplotlib, numpy.  Display mathematics uses
MathText's vector glyph positions.  Inline mathematics is rendered at 600 dpi.
This file builds presentation artefacts; it is not a mathematical verifier.
"""
from pathlib import Path
import hashlib
import html
import re
import sys
import argparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser, math_to_image
from matplotlib.font_manager import FontProperties
import numpy as np

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, Image, Flowable, KeepTogether)

options = argparse.ArgumentParser(description=__doc__)
options.add_argument('--package-dir', type=Path)
options.add_argument('--output', type=Path)
options.add_argument('--cache-dir', type=Path)
args = options.parse_args()
HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
default_package = HERE.parent.parent if HERE.parent.name == 'code' else ROOT / 'output/evidence_press_binary_quadratic_v1_0_0'
PKG = (args.package_dir or default_package).resolve()
SOURCE = PKG / 'manuscript/binary-quadratic-informational-substitutes.md'
OUT = (args.output or PKG / 'manuscript/binary-quadratic-informational-substitutes.pdf').resolve()
FIGS = PKG / 'figures'
CACHE = (args.cache_dir or PKG / 'build/inline_math').resolve()
for folder in [OUT.parent, FIGS, CACHE]:
    folder.mkdir(parents=True, exist_ok=True)

matplotlib.rcParams.update({'mathtext.fontset': 'dejavuserif',
                            'font.family': 'DejaVu Sans',
                            'axes.spines.top': False,
                            'axes.spines.right': False})

def draw_figure():
    q = np.linspace(0, 1, 701)
    h = 49/256 - .25 * ((3/16)/(.75-.5*q) + (3/16)/(.25+.5*q))
    plum, ochre, ink, cream = '#75425E', '#AB752F', '#303039', '#FCFAF6'
    fig, ax = plt.subplots(figsize=(8.4, 4.2), constrained_layout=True)
    fig.patch.set_facecolor(cream); ax.set_facecolor(cream)
    ax.axhline(0, color=ink, lw=.8)
    ax.fill_between(q, h, 0, where=h<0, color=plum, alpha=.09)
    ax.fill_between(q, h, 0, where=h>=0, color=ochre, alpha=.16)
    ax.plot(q, h, color=plum, lw=2.4)
    ax.scatter([0,.25,.5,1],[-15/256,-11/1280,1/256,-15/256],
               color=[plum,plum,ochre,plum],s=32,zorder=5)
    ax.annotate('No disclosure: q = 1/2\nH(q) = 1/256 > 0',
                xy=(.5,1/256),xytext=(.62,-.012),fontsize=9,color=ink,
                arrowprops={'arrowstyle':'-','color':ochre,'lw':1})
    ax.annotate('Mixed report: q = 1/4\nH(q) = -11/1280 < 0',
                xy=(.25,-11/1280),xytext=(.10,-.035),fontsize=9,color=ink,
                arrowprops={'arrowstyle':'-','color':plum,'lw':1})
    ax.set_xlabel('Posterior q = P(B = 1 | disclosure)',fontsize=10)
    ax.set_ylabel('Oriented residual H(q)',fontsize=10)
    ax.set_xlim(-.025,1.025); ax.set_ylim(-.068,.014)
    ax.set_xticks([0,.25,.5,.75,1]); ax.tick_params(labelsize=9)
    ax.grid(axis='y',alpha=.17,color=ink)
    ax.set_title('A whole-signal comparison can miss a disclosure failure',
                 loc='left',fontsize=12,pad=13,color=ink,weight='bold')
    fig.savefig(FIGS/'disclosure-residual.png',dpi=240)
    fig.savefig(FIGS/'disclosure-residual.svg')
    plt.close(fig)

registered = {}
def register_font(path):
    path = str(path)
    if path not in registered:
        name = 'MathFont' + hashlib.sha256(path.encode()).hexdigest()[:10]
        pdfmetrics.registerFont(TTFont(name,path))
        registered[path] = name
    return registered[path]

fontdir = Path(matplotlib.get_data_path()) / 'fonts/ttf'
for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),
                  ('BodyItalic','DejaVuSerif-Italic.ttf'),('Sans','DejaVuSans.ttf'),
                  ('SansBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')

parser = MathTextParser('path')

class MathBlock(Flowable):
    def __init__(self, expression, fontsize=10.9):
        Flowable.__init__(self)
        expression = expression.replace(r'\mathbb E', r'\mathbb{E}')
        self.expression = expression
        self.vector = parser.parse('$'+expression+'$',dpi=72,
                                   prop=FontProperties(size=fontsize))
        self.spaceBefore=4; self.spaceAfter=8
    def wrap(self, availWidth, availHeight):
        self.scale = min(1,availWidth/float(self.vector.width))
        self.width = availWidth
        self.height = float(self.vector.height)*self.scale+8
        return self.width,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.translate((self.width-float(self.vector.width)*self.scale)/2,
                    float(self.vector.depth)*self.scale+3)
        c.scale(self.scale,self.scale)
        for font,fontsize,num,x,y in self.vector.glyphs:
            c.setFont(register_font(font.fname),fontsize)
            c.drawString(x,y,chr(num))
        for x,y,w,h in self.vector.rects:
            c.rect(x,y,w,h,stroke=0,fill=1)
        c.restoreState()

def inline_math(expression,size=9.4):
    expression = expression.replace(r'\mathbb E', r'\mathbb{E}')
    key=hashlib.sha256((str(size)+expression).encode()).hexdigest()
    target=CACHE/(key+'.png')
    prop=FontProperties(size=size)
    v=parser.parse('$'+expression+'$',dpi=72,prop=prop)
    if not target.exists():
        math_to_image('$'+expression+'$',str(target),prop=prop,dpi=600,
                      format='png',color='#222229')
    return '<img src="%s" width="%.3f" height="%.3f" valign="%.3f"/>' % (
        target, float(v.width),float(v.height),-float(v.depth))

def rich(text,size=9.4):
    pieces=[]; pos=0
    for match in re.finditer(r'\$([^$\n]+)\$',text):
        pieces.append(html.escape(text[pos:match.start()]));
        pieces.append(inline_math(match.group(1),size)); pos=match.end()
    pieces.append(html.escape(text[pos:])); result=''.join(pieces)
    result=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',result)
    result=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',result)
    result=re.sub(r'https://[^\s<]+',lambda m:'<link href="'+m[0]+'" color="#68435B">'+m[0]+'</link>',result)
    return result

INK=colors.HexColor('#27272F'); PLUM=colors.HexColor('#68435B')
styles={
    'body':ParagraphStyle('body',fontName='Body',fontSize=9.45,leading=14.35,
                          spaceAfter=7.3,textColor=INK,allowWidows=0,allowOrphans=0),
    'title':ParagraphStyle('title',fontName='SansBold',fontSize=22.5,leading=27,
                           spaceAfter=12,textColor=PLUM),
    'subtitle':ParagraphStyle('subtitle',fontName='Sans',fontSize=13.5,leading=18,
                              spaceAfter=14,textColor=INK),
    'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=12.5,leading=16.5,
                        spaceBefore=17,spaceAfter=9,textColor=PLUM,keepWithNext=True),
    'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=10.35,leading=14,
                        spaceBefore=10,spaceAfter=7,textColor=INK,keepWithNext=True),
    'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8.1,leading=11.2,
                             spaceAfter=10,textColor=INK),
    'meta':ParagraphStyle('meta',fontName='Sans',fontSize=8.5,leading=12,
                          spaceAfter=16,textColor=INK),
    'cell':ParagraphStyle('cell',fontName='Body',fontSize=9,leading=13.5,textColor=INK),
}

def make_story(source):
    lines=source.splitlines(); story=[]; i=0; firsth2=True
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line=='$$':
            expr=[];i+=1
            while i<len(lines) and lines[i].strip()!='$$': expr.append(lines[i].strip());i+=1
            story.append(MathBlock(' '.join(expr)));i+=1;continue
        if line.startswith('# '):
            story.append(Paragraph(rich(line[2:]),styles['title']));i+=1;continue
        if line.startswith('## '):
            text=line[3:]
            style='subtitle' if firsth2 else 'h2';firsth2=False
            story.append(Paragraph(rich(text),styles[style]));i+=1;continue
        if line.startswith('### '):
            story.append(Paragraph(rich(line[4:]),styles['h3']));i+=1;continue
        if line.startswith('Evidence Press research candidate'):
            story.append(Paragraph(rich(line),styles['meta']));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                raw=lines[i].strip()
                if not re.match(r'^\|[-:| ]+\|$',raw):
                    rows.append([Paragraph(rich(cell.strip(),9),styles['cell'])
                                 for cell in raw.strip('|').split('|')])
                i+=1
            t=Table(rows,colWidths=[104,142,225],repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EEE7EB')),
                ('LINEBELOW',(0,0),(-1,0),.65,PLUM),
                ('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#DCD6D8')),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),7),
                ('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            lead=story.pop()
            heading=story.pop()
            story.append(KeepTogether([heading,lead,Spacer(1,4),t,Spacer(1,12)]));continue
        if line.startswith('!['):
            m=re.match(r'!\[(.*?)\]\((.*?)\)',line)
            if m:
                figpath=(SOURCE.parent/m[2]).resolve()
                story.append(KeepTogether([Image(str(figpath),width=470,height=235),
                    Paragraph(rich(m[1]),styles['caption'])]))
            i+=1;continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','$$','|','![')):
            para.append(lines[i].strip());i+=1
        paragraph=' '.join(para)
        # Keep short theorem announcements with at least the next display.
        st=styles['body']
        item=Paragraph(rich(paragraph),st)
        following=next((x.strip() for x in lines[i:] if x.strip()),'')
        if following.startswith('|'):
            item.keepWithNext=True
        if paragraph.startswith('**Corollary 2.1'):
            item=KeepTogether([item])
        story.append(item)
    return story

def frame(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(colors.HexColor('#D7CDD3'));canvas.setLineWidth(.4)
    canvas.line(57,h-40,w-57,h-40)
    canvas.setFillColor(PLUM);canvas.setFont('Sans',7.2)
    canvas.drawString(57,h-31,'EVIDENCE PRESS  /  RESEARCH CANDIDATE')
    canvas.setFillColor(colors.HexColor('#62616A'));canvas.setFont('Sans',7.2)
    canvas.drawString(57,31,'Binary informational substitutes · Quadratic scoring · 8 October 2026')
    canvas.drawRightString(w-57,31,str(doc.page));canvas.restoreState()

def main():
    draw_figure()
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=57,leftMargin=57,
        topMargin=57,bottomMargin=53,title='Four tests for binary informational substitutes',
        author='Anonymous',subject='Complete binary quadratic-scoring classification')
    doc.build(make_story(SOURCE.read_text()),onFirstPage=frame,onLaterPages=frame)
    print(OUT)

if __name__=='__main__':main()
