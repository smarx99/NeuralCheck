// components/Sidebar.tsx
import React, {RefObject} from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import { BsClipboardData } from "react-icons/bs";
import { MdOutlineAccountCircle } from "react-icons/md";
import { Link } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
  datasets: string[];
  onUploadDataset: (event: React.ChangeEvent<HTMLInputElement>) => void;
  fileInputRef: RefObject<HTMLInputElement>;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar, datasets, onUploadDataset, fileInputRef}) => {
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
            <div className="flex items-center">
              {isOpen && <span className="text-xl mr-4"><BsClipboardData /></span>}
              <span className={`${isOpen ? 'block' : 'hidden'}`}>Datasets</span>
            </div>
          </li>
          {datasets.map((dataset, index) => (
            <li key={index} className="p-2 pl-8">
              {isOpen && (
                <span className="flex items-center">
                  <BsClipboardData className="mr-2" />
                  <span className="block">{dataset}</span>
                </span>
              )}
            </li>
          ))}
          <li className="p-2 pl-8">
            <input
              type="file"
              accept=".csv"
              onChange={onUploadDataset}
              ref={fileInputRef}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer flex items-center">
              {isOpen && <span className="text-xl mr-4">+</span>}
              <span className={`${isOpen ? 'block' : 'hidden'}`}>Upload Dataset</span>
            </label>
          </li>
          <li className="p-2">
            {isOpen && (
              <Link to="/account" className="flex items-center">
                <span className="text-xl mr-4"><MdOutlineAccountCircle /></span>
                <span className={`${isOpen ? 'block' : 'hidden'}`}>Account</span>
              </Link>
            )}
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
