import { useState, useCallback } from 'react';

import { initialize, get_app_state, auth_states } from './appcontoller'

import { Header } from './components/Header'
import { Authorization } from './frames/Authorization';
import { Loader } from './frames/Loader'

function App() {

  const [, updateState] = useState();
  const rerender = useCallback(() => updateState({}), []);

  initialize().then((need_rerender) => { if (need_rerender) rerender(); })

  let app_state = get_app_state()

  let body = <Loader />

  if (auth_states.includes(app_state))
    body = <Authorization rerender={rerender}/>

  return (
    <div>
      <Header />
      { body }
    </div>
  );
}

export default App;
