import { get_app_state } from './appcontoller'
import { Header } from './components/Header'


function App() {

  let app_state = get_app_state()


  return (
    <div data-bs-theme="light">
      <Header />
    </div>
  );
}

export default App;
