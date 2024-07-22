import { useState, useCallback } from 'react';

import { initialize, get_app_state, auth_states } from './appcontoller'

import { Header } from './components/Header'
import { Authorization } from './frames/Authorization';
import { Loader } from './frames/Loader'

function App() {

  const [, updateState] = useState();
  const forceUpdate = useCallback(() => updateState({}), []);

  initialize().then((rerender) => { if (rerender) forceUpdate(); })

  let app_state = get_app_state()

  let body = <Loader />

  if (auth_states.includes(app_state))
    body = <Authorization />

  return (
    <div data-bs-theme="light">
      <Header />
      { body }
    </div>
  );
}

export default App;
