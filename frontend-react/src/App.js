import React,{useState, useEffect} from 'react';
import {Preview} from './components/Preview';
import {Routes, Route} from 'react-router-dom';
import Home from './components/Home';
import Nlp from './components/Nlp';
function App() {
  
  return (
    <>
      <Routes> 
        <Route path ='/' element={<Home />}/>
        <Route path='/engine' element={<Nlp />}/>
      </Routes>


    </>
  );
}

export default App;
