import { Books, Hand, House, Info, NotePencil } from 'phosphor-react';
import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <div className="navbar">
      <NavLink to="/" data-theme="red">
        <House size={40} />
        <div>Home</div>
      </NavLink>
      <NavLink to="/about" data-theme="orange">
        <Info size={40} />
        <div>About</div>
      </NavLink>
      <NavLink to="/book" data-theme="green">
        <Books size={40} />
        <div>Books</div>
      </NavLink>
      <NavLink to="/notes" data-theme="blue">
        <NotePencil size={40} />
        <div>Notes</div>
      </NavLink>
      <NavLink to="/sign" data-theme="purple">
        <Hand size={40} />
        <div>Sign</div>
      </NavLink>
    </div>
  );
}

export default Navbar;
