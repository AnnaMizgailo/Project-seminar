"""Generate info from api and provide a web interface for it"""
from flask import Flask, redirect
import resume_manipulator

app = Flask(__name__, static_url_path="", static_folder="public")


@app.route("/", methods=["GET","POST"])
def generate_resume():
    '''
    Get resume from .txt
    '''
    return resume_manipulator.generate_resume()

@app.route("/resume/regenerate", methods=["GET","POST"])
def regenerate_resume():
    '''
    Regenerate resume
    '''
    redirect('')
    return resume_manipulator.generate_resume()

if __name__ == '__main__':
    resume_manipulator.generate_resume()
    app.run(host='0.0.0.0', port=1301, debug=False)