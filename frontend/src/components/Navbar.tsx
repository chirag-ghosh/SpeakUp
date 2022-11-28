import { Books, Hand, House, Info, NotePencil } from 'phosphor-react';
import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <div className="navbar">
      <NavLink to="/">
        <House size={40} />
        <div>Home</div>
      </NavLink>
      <NavLink to="/about">
        <Info size={40} />
        <div>About</div>
      </NavLink>
      <NavLink to="/book">
        <Books size={40} />
        <div>Books</div>
      </NavLink>
      <NavLink to="/notes">
        <NotePencil size={40} />
        <div>Notes</div>
      </NavLink>
      <NavLink to="/sign">
        <Hand size={40} />
        <div>Sign</div>
      </NavLink>
    </div>
  );
}

export default Navbar;
