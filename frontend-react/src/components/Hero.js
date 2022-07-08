import React from 'react'
import {FaDatabase, FaAsterisk, FaAccusoft, FaFacebook, FaTwitter, FaGithub} from 'react-icons/fa'
import './HeroStyles.css'
const Hero = () => {
  return (
    <div className='hero'>
        <div className = 'content'>
            <div className = 'col-1'>
                <h1> Online NLP Engine  </h1>
                <h1><span className='primary-color'>Patent Parser</span></h1>
                <p>
                    Upload your Patent PDF files to be parsed
                    using our NLP-engine.  
                </p>
                
            </div>
            <div className='login'>
                <h1> Sign-in using your QCRI credentials
                </h1>
                <label className = 'label'> E-mail</label> <br/>
                <input className ='input' type="text" name="uname" required /><br/><br/>
                <label className = 'label' type = "password"> Password</label> <br/>
                <input className ='input' type ='password' required />
                <button className = 'button-27'> Sign-in </button>


               

            </div>
                
            














        </div>

    </div>
  )
}

export default Hero
