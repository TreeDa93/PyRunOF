import pathlib as pl

txt_path = pl.Path().cwd() / 'testold_old.txt'
cwd_path = pl.Path.cwd()
print(txt_path.exists())

new_name = 'test.txt'
new_txt_path = txt_path.parent / new_name

print(type(txt_path.stem))
print(txt_path.stem)

txt_path.replace(new_txt_path)