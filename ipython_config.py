# coding=utf8
c = get_config()
app = c.InteractiveShellApp

app.exec_files = [b'prompt_functions.py']

# This can be used at any point in a config file to load a sub config
# and merge it into the current one.
load_subconfig('ipython_config.py', profile='default')


# c.PromptManager.in_template = r'{color.LightGreen}\u@\h{color.LightBlue}[{color.LightCyan}\Y1{color.LightBlue}]{color.Green}|\#> '
# c.PromptManager.in2_template = r'{color.Green}|{color.LightGreen}\D{color.Green}> '
# c.PromptManager.out_template = r'<\#> '
c.PromptManager.in_template = ur'{color.Red}\u279c {color.LightCyan}\Y3{color.Blue}{git_branch_and_st} '
c.PromptManager.in2_template = r'{color.Green}|{color.LightGreen}\D{color.Green}> '
c.PromptManager.out_template = r'<\#> '

c.PromptManager.justify = True

c.InteractiveShell.separate_in = ''
c.InteractiveShell.separate_out = ''
c.InteractiveShell.separate_out2 = ''
c.InteractiveShell.confirm_exit = False
c.InteractiveShell.implicit_cd = True
c.InteractiveShell.term_title = True

c.Completer.case_insensitive = True

c.PrefilterManager.multi_line_specials = True

lines = """
%rehashx
"""

# You have to make sure that attributes that are containers already
# exist before using them.  Simple assigning a new list will override
# all previous values.
if hasattr(app, 'exec_lines'):
    app.exec_lines.append(lines)
else:
    app.exec_lines = [lines]
    
c.AliasManager.user_aliases = [
    ('ls', 'ls -G'),
    ('l', 'ls -G'),
]