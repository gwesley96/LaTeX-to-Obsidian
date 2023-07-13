# CONVERTING TO MARKDOWN FOR OBSIDIAN
import re
import subprocess


def pandoc_convert(input_text):
    # Define the file path for the temporary Markdown file  
    file_path = '/Users/greysonwesley/Desktop/DONOTDELETE/convert.md'

    # Save the input text to the temporary Markdown file
    with open(file_path, 'w') as file:
        file.write(input_text)

    # Command to run Pandoc in the terminal
    command = ["pandoc", file_path, "-f", "latex", "-t", "commonmark_x"]
    try:
        # Run the command and capture the output
        output = subprocess.check_output(command, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed with error: {e}")
        return None

def copy_to_clipboard(text):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE
    )
    process.communicate(text.encode('utf-8'))

def paste_from_clipboard():
    process = subprocess.Popen(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}, stdout=subprocess.PIPE
    )
    output, _ = process.communicate()
    return output.decode('utf-8').strip()


# ACTUAL PROGRAM:
def automate_process(input_latex):
    text = paste_from_clipboard() # start with the input to automate_process
    text = re.sub(r'\\hint\{(.*?)\}', r'\1', text, re.DOTALL)
    text = re.sub(r'\s\\problem\{(.*?)\}\s', r'\n\\textbf{PROBLEM}. (\\emph{\1})\n\n', text, flags=re.DOTALL)
    text = re.sub(r'\s\\part\s', r'\n\\textbf{SOLNPART}\n\n', text, flags=re.DOTALL)
    text = re.sub(r'\s\\solution\s', r'\n\\textbf{SOLN}\n\n', text, flags=re.DOTALL)

    text = re.sub(r'\\end\{mdframed\}',r' ',text,flags=re.DOTALL)
    text = re.sub(r'\\begin\{mdframed\}',r' ',text,flags=re.DOTALL)
    text = text.replace("rep}","}")
    text = re.sub(r'\\qedhere',r'',text)
    text = text.replace("ointctrclockwise","oint")
    text = re.sub(r'\\begin\{align\*}\s*?\[',r'\\begin{align*} \[', text, flags=re.DOTALL) # text = re.sub(r'\\\[([\s\S]*?)\\\]', r'\n\n\1\n\n', text,flags=re.DOTALL)
    text = re.sub(r'\\begin\{(.*?)\}\[(.*?)\]',r'\\begin{\1} (\\emph{\2}).', text, flags=re.DOTALL) # text = re.sub(r'\\\[([\s\S]*?)\\\]', r'\n\n\1\n\n', text,flags=re.DOTALL)
    text = re.sub(r'\%\s(https[\s\S]*?)\s+(\\\[[\s\S]*?\\\])', r'\n\1\n', text, flags=re.DOTALL)
    text = re.sub(r'%.*?\n',r' ',text,flags=re.DOTALL) # should be AFTER the tikz thing above
    text = re.sub(r'\\defn\{(.*?)\}', r'\\textbf{\1}', text, flags=re.DOTALL)    
    text = re.sub(r'\\underline\{(.*?)\}', r'\\emph{\1}', text, flags=re.DOTALL)    
    text = text.replace("{description}","{itemize}")
    text = text.replace("{enumerate}","{itemize}")
    # text = re.sub(r'\s*\\\\\s*',r' \\\\ ')
    # text = re.sub(r'\\begin\{.*?\}\s*',r'\\begin{\1} ')
    # text = re.sub(r'\n\\end\{.*?\}',r' \\end{\1} ')
    
    text = pandoc_convert(text) # use pandoc conversion on what we have so far

    text = re.sub(r'\$\$\\begin\{tikzcd\}[\s\S]*?\\end\{tikzcd\}\$\$', r' ', text, flags=re.DOTALL)
    text = re.sub(r'\s+(https[\s\S]*?)(?=\n)\s+', r'<iframe class="quiver-embed" src="\1&macro_url=https://gist.githubusercontent.com/gwesley96/aa003342fcc08c40cd10353da2b130f8/raw/585d934c6c364a1924723d52bfd45c6f9e08506a/GreyTeX.sty&embed" style="width:100%;height:100%;border-radius: 8px; border: none;"></iframe>', text, flags=re.DOTALL)
    text = text.replace("{aligned}","{align*}")
    text = text.replace("{gathered}","{align*}")
    
    text = re.sub(r'\s*\:\:\:\n', r'\n', text, flags=re.DOTALL) 
    text = re.sub(r'\:\:\: \{\.(.*?)\}(?!\s*[^\n]\(\*.*?\*\)\.)', lambda match: f'###### **{match.group(1).capitalize()}.**\n\n', text, flags=re.DOTALL)  # Responsible for the bold "**Theorem.** "
    text = re.sub(r'\[\]\{\#.*?label\="(.*?)"\}', r'(*\1*).', text, flags=re.DOTALL) # Responsible for the italic "(* alternate title option *). "
    
    text = re.sub(r'(?<!\n)\n(?!\n)',r' ',text,flags=re.DOTALL) # remove all line breaks
    text = re.sub(r'(?!\n)\s{2,}',r' ',text,flags=re.DOTALL) # remove two or more consecutive spaces after removing all line breaks
    
    text = re.sub(r'(\#\#\#\#\#\#\s\*\*\w+\.\*\*)\s*', r'\n\1 ',text,flags=re.DOTALL) # changes environment into just bold text starting a line
    text = re.sub(r'\$\$\\begin\{align\*\}\s*(.*?)\s*\\end\{align\*\}\$\$', r'$$\\begin{align*}\1\\end{align*}$$', text, flags=re.DOTALL) # properly reformat align environments after removing all line breaks
    text = text.replace("mapsfrom","from")
    text = text.replace("*Proof.* ", "")
    text = text.replace("Tinyproof","Proof")
    # text = re.sub(r'\s*\$\$(.*?)\$\$\s*', r'$$\1$$', text, flags=re.DOTALL)
    text = text.replace("---",'—')
    text = text.replace("--",'–')
    text = re.sub(r'\n*?\#\#\#\#\#\#\s\*\*Proof\.\*\*', r'\n```blindfold\n*Proof.*',text,flags=re.DOTALL)
    # text = re.sub(r'\#\#\#\#\#\#\s\*Proof\.\*', r'*Proof.*',text,flags=re.DOTALL)
    
    text = re.sub(r'◻', r'$\\square$\n```',text,flags=re.DOTALL)
    text = re.sub(r'\\Tr(?=\W)', r'\\tr',text,flags=re.DOTALL)
    text = re.sub(r'\s*\#\#\#\#\#\#',r'\n\n######',text,flags=re.MULTILINE)
    text = re.sub(r'\\tag\{(.*?)\}',r'\\qquad\\text{(\1)}',text,flags=re.DOTALL)
    # text = re.sub(r'(\#\#\#\#\#\#\s.*?)\n(\(\*.*?\*\)\.)\s*(?!\n)',r'\1 \2\n',text, flags=re.DOTALL)
    text = text.replace("**PROBLEM**.", "###### **Exercise.**")
    text = text.replace("**SOLNPART**", "###### **Solution to the next part.**")
    text = text.replace("**SOLN**", "###### **Solution.**")
    text = text.replace("$,",",$")
    text = text.replace("$.",".$")
    text = re.sub(r'\(\*(\w)(.*?)\*\)', lambda m: f"(*{m.group(1).upper()}{m.group(2)}*)", text, flags=re.DOTALL)
    re.sub(r'\(\*(\w)(.*?)\*\)',r'(*\2*)',text,flags=re.DOTALL)
    # text = re.sub(r'(\#\#\#\#\#\s\*\*.*?\*\*\s\(\*.*?\*\)\.)\n',r'\1\s',text, flags=re.DOTALL)
    text = text.replace("###### ","")
    text = text.replace("\[","[")
    text = text.replace("**Center.** ","")
    text = re.sub(r'\n*\s*?\$\$\s*(.*?)\s*?\$\$\s*\n*\s*',r'$$\1$$',text,flags=re.DOTALL)
    text = re.sub(r'\$\$\*\*(\w+?)\.\*\*',r'$$\n**\1.**',text,flags=re.DOTALL)
    text = re.sub(r'\$\$```',r'$$\n```',text,flags=re.DOTALL)
    text = text.replace("$).",").$")
    replace ```(?!\w)\n+?(?=.) with ```\n\n
    return text


def automate_process_clipboard(): 
    clipboard = paste_from_clipboard()
    copy_to_clipboard(automate_process(clipboard))

# copy_to_clipboard(latex)
automate_process_clipboard()


  



