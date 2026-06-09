'''this script is to test whether the minimal example can work. if not,
please check the installation of the package.

Reference
---------
https://gradio.app/guides/custom-HTML-components
https://3dmol.csb.pitt.edu/doc/tutorial-embeddable.html
'''
import gradio as gr

html = ''' 
<div style="height: 400px; width: 400px; position: relative;" 
     class='viewer_3Dmoljs' 
     data-pdb='2POR' 
     data-backgroundcolor='0xffffff' 
     data-style='stick' 
     data-ui='true'></div>
'''

head = (
    '<script src="https://3Dmol.org/build/3Dmol-min.js"></script>'     
    '<script src="https://3Dmol.org/build/3Dmol.ui-min.js"></script>'  
)

with gr.Blocks() as demo:
    viewer =gr.HTML(
        value=html,
        label='Protein visualization',
        head=head,
        js_on_load='$3Dmol.autoload();'
    )

if __name__ == '__main__':
    demo.launch()
