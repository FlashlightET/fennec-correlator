# fennec-correlator
extract the "true colors" of anime characters (kemono friends originally as per the repo name but can be used for all sorts of color extraction use cases) based on isolated regions from screenshots

![image](https://github.com/FlashlightET/fennec-correlator/assets/29938499/6561707f-9e71-426d-855b-4d860deb59d5)

originally developed (and used) as a tool for making more accurate Kemono Friends 3d models 

TODO: comment code and make repo public

PROCESS:

1. Make a folder of anime screenshots.
2. Copy that folder
3. Rename it to like character_hair or something
4. Isolate that region from each screenshot in the new folder in like paint.net or something
5. Change some variables in `Fennec Correlator FolderBased.py`
6. Let it do its thing
7. Go to the `fennec_colorrefs` and find the file with a good bit of data like level 0 or 1 or something
8. Color pick the best color manually
9. ???
10. Save your findings to a file, repeat for every major color component on the character

# Character colors extracted with this program
## Fennec
```
                                        skin: F9EAE3
                                      shadow: E6C3B6
                                       shirt: ECC1BD
                                       skirt: F1F1F3
hair top/ears yellow/arms yellow/bowtie/tail: FBE8B4
                                 hair bottom: FAD67E
                                  hair white: F7F7ED
                                   ears pink: F2CFCF
                             eyes dark brown: 1B110E
                          eyes lighter brown: 4E2F26
                        eyes highlight olive: 826F40
                                 eyes sclera:
                                eyes shading:
                                 hair strand: 4E495F
                                 neck shadow: F2DDC8
```

Uhh have tyhis for now ![image](https://github.com/FlashlightET/fennec-correlator/assets/29938499/7c824cc2-433d-4ac6-84da-337f8aef8157)
