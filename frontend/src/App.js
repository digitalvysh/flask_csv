import './App.css';

import React from 'react'
import Date from './components/Date';
import Upload from './components/Upload';

const App = () => {
  return (
    <div>
      <div>
        <Upload/>
      </div>
      <div>
        <Date />
      </div>
    </div>

  )
}

export default App