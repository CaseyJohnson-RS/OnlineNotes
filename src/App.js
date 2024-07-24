import { useState, useCallback } from 'react';

import { initialize, get_app_state, auth_states } from './appcontoller'

import { Row, Col } from 'react-bootstrap';

import { Header } from './components/Header'
import { Authorization } from './frames/Authorization';
import { MainPage } from './frames/MainPage'
import { Loader } from './frames/Loader'

function App() {

  const [, updateState] = useState();
  const rerender = useCallback(() => updateState({}), []);

  initialize().then((need_rerender) => { if (need_rerender) rerender(); })

  let app_state = get_app_state()

  let body = <Loader />

  if (auth_states.includes(app_state))

    body = <Authorization parent_rerender={rerender}/>

  else if (app_state === "main-page")
  
    body = <MainPage app_rerender={rerender}/>
    
  return (
    <div>
      <Header app_rerender={rerender}/>
      <Row>
        <Col xs={1}/>
        <Col xs={10}>
        { body }
        </Col>
        <Col xs={1}/>
      </Row>
    </div>
  );
}

export default App;
