import React from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import { Link } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar }) => {
  return (
    <div className={`fixed top-0 left-0 h-full ${isOpen ? 'w-60' : 'w-16'} bg-blue-800 text-white transition-width duration-300`}>
      <div className="flex items-center justify-between p-4">
        <h1 className={`text-xl font-bold ${isOpen ? 'block' : 'hidden'}`}>NeuralCheck</h1>
        <button onClick={toggleSidebar} className="focus:outline-none">
          {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
        </button>
      </div>
      <nav className="mt-10">
        <ul>
          <li className="p-2">
            <Link to="/app" className="flex items-center">
              <span className="text-xl mr-4">🏠</span>
              <span className={`${isOpen ? 'block' : 'hidden'}`}>Home</span>
            </Link>
          </li>
          <li className="p-2">
            <Link to="/datasets" className="flex items-center">
              <span className="text-xl mr-4">📊</span>
              <span className={`${isOpen ? 'block' : 'hidden'}`}>Datasets</span>
            </Link>
          </li>
          <li className="p-2">
            <Link to="/login" className="flex items-center">
              <span className="text-xl mr-4">🔐</span>
              <span className={`${isOpen ? 'block' : 'hidden'}`}>Logout</span>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
