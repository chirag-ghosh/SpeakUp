import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Narrration from './pages/Narration';
import Home from './pages/Home';
import Notes from './pages/Notes';
import SignLanguage from './pages/SignLanguage';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route index element={<Home />} />
          <Route path="notes" element={<Notes />} />
          <Route path="narration" element={<Narrration />} />
          <Route path="sign" element={<SignLanguage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
