import React from 'react';
import {useState} from 'react';
import './NLPStyles.css';
import Navbar from './Navbar';
import axios from 'axios';

export const Nlp = () => {
  const [file, setfile] = useState(null);
  const [data,setData] = useState([{}])
  const [data2,setData2] = useState([{}])
  const[data3, setData3] = useState([{}])
  
  const onInputChange = (e) => {
    console.log(e.target.files[0])
    fetch(`http://localhost:5000/engine/process/${e.target.files[0].name}`, {
          method: "GET", 
          // mode: 'no-cors',
          headers:{
            "Content-Type" : "application/json",
          },
        }).then(
        res => {console.log(res); return res.json();}
    ).then(
        res => {
            setData(res)
            console.log(res)

        }
    )
} 
const onInputChange2 = (e) => {
  console.log(e.target.files[0])
  fetch(`http://localhost:5000/engine/process/${e.target.files[0].name}`, {
        method: "GET", 
        // mode: 'no-cors',
        headers:{
          "Content-Type" : "application/json",
        },
      }).then(
      res => {console.log(res); return res.json();}
  ).then(
      res => {
          setData2(res)
          console.log(res)

      }
  )
} 

  const onFinalChange = () => {
    if (data.name !== undefined && data2.name !== undefined) {
      const body = {d1: data, d2: data2}
      axios.post(`http://localhost:5000/engine/comparison/`, body).then(
        res => {
            setData3(res.data) 
            console.log(res.data)

        }
    )

  }
}
  const onSubmit = (e) => {
    e.preventDefault();
  };

  const dataSent = {
    Name: data["name"],
    19: data["(19)"],
    10: data["(10)"],
    12:data["(12)"],
    21: data["(21)"],
    22: data["(22)"],
    30:data["(30)"],
    43: data["(43)"],
    51: data["(51)"],
    52:data["(52)"],
    54: data["(54)"],
    71: data["(71)"],
    72:data["(72)"],
    Star :data["(**)"],
    57:data["(57)"]
  }

  axios.post('https://sheet.best/api/sheets/ec592633-8dcb-4519-8700-3a34f208029a',dataSent)
  return (
    
      
    <div className="NLP"> 
      <Navbar/>
      <div className='form-container'>
        <form method="post" action="#" id="#" onSubmit = {onSubmit}>
            <div className="form-group files">
              <label className='firstFile'>Upload your first file </label>
              <input type="file" onChange = {onInputChange} style={{ justifyContent:'center', }} multiple=""/>
            </div>
            
        
        </form>

        <form method="post" action="#" id="#" onSubmit = {onSubmit}>
            <div className="form-group files">
              <label className='secondFile'>Upload your second file </label>
              <input type="file" onChange = {onInputChange2} className="form-control" multiple=""/>
            </div>
            
        
        </form>
      </div>
      
      {data['name'] !== undefined && data2['name'] == undefined && 
      <div class="card">
        <h1>Loading...</h1>
        <p>Your patents will soon be extracted</p>
        <div class="loader">
          <div class="spin"></div>
          <div class="bounce"></div>
        </div>
      </div>}
      {data['name'] !== undefined && data2['name'] !== undefined &&
        <div className = 'images-container'>
          <div className='image'>
            {data['name'] !== undefined && <img style={{maxWidth: '500px'}} src={`http://localhost:5000/getImage/${data["name"]}` }/>}
            <div className='description'>
              <h2> {data['name'] !== undefined && data.name}</h2>


            </div>
          </div>
          <div className='image'>
            {data2['name'] !== undefined && <img style={{maxWidth: '500px'}} src={`http://localhost:5000/getImage/${data2["name"]}` }/>}
            <div className='description'>
              <h2> {data2['name'] !== undefined && data2.name}</h2>


            </div>
          </div>
        
        </div>
}
{data['name'] !== undefined && data2['name'] !== undefined &&
      <div className='results-containers'>
        <div className = 'results-container' >
          <p>  {Object.keys(data).length > 0 && data["(19)"]} </p>
          {Object.keys(data).length > 1 && 
            Object.keys(data).map((key, idx) => {
                if(key !== 'name'){
                  return (
                  <p key={idx}> {key} {key.length > 0 && data[key]} </p>
                )}
          })}
          </div>
          <div className = 'results-container2' >
            <p>  {Object.keys(data).length > 0 && data["(19)"]} </p>
            {Object.keys(data2).length > 1 && 
              Object.keys(data2).map((key, idx) => {
                  if(key !== 'name'){
                    return (
                    <p key={idx} style={{fontStyle:
                      Object.keys(data3).includes(key) ? 'italic':''}}> {key} {key.length > 0 && data2[key]} </p>
                  )}
            })}
          </div>
        </div>}
        {data['name'] !== undefined && data2['name'] !== undefined &&
        <button className = 'button-27' onClick={() => {
          data['name'] !== undefined && data2['name'] !== undefined && onFinalChange()
        }}> Compare </button>}


      </div> 
  ); 
} 
 
export default Nlp
