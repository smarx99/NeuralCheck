// components/Sidebar.tsx
import React, { RefObject, useState } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import { BsClipboardData } from "react-icons/bs";
import { MdOutlineAccountCircle } from "react-icons/md";
import { AiOutlineQuestionCircle } from "react-icons/ai";
import { Link } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
  datasets: string[];
  onUploadDataset: (event: React.ChangeEvent<HTMLInputElement>) => Promise<{ success: boolean; message?: string }>;
  fileInputRef: RefObject<HTMLInputElement>;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar, datasets, onUploadDataset, fileInputRef }) => {
const [showTooltip, setShowTooltip] = useState(false);
const [uploadError, setUploadError] = useState<string | null>(null);
const [uploadMessage, setUploadMessage] = useState<string>('');

const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
  setUploadError(null); // Clear previous errors
  setUploadMessage(''); // Clear previous messages
  const result = await onUploadDataset(event);
  if (result.success) {
    setUploadMessage('Upload successful!');
  } else {
    setUploadError(result.message || 'Error uploading dataset. Please try again.');
  }
};

  return (
    <div className={`fixed top-0 left-0 h-full ${isOpen ? 'w-60' : 'w-16'} bg-blue-800 text-white transition-width duration-300`}>
      <div className="flex items-center justify-between p-4">
        <Link to="/app" className={`text-xl font-bold ${isOpen ? 'block' : 'hidden'}`}>NeuralCheck</Link>
        <button onClick={toggleSidebar} className="focus:outline-none">
          {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
        </button>
      </div>
      <nav className="mt-10">
        <ul>
          <li className="p-2 flex items-center">
            <div className="flex items-center">
              {isOpen && <span className="text-xl mr-4"><BsClipboardData /></span>}
              <span className={`${isOpen ? 'block' : 'hidden'}`}>Datasets</span>
            </div>
            {isOpen && (
              <span 
                className="ml-2 relative" 
                onMouseEnter={() => setShowTooltip(true)} 
                onMouseLeave={() => setShowTooltip(false)}
              >
                <AiOutlineQuestionCircle />
                {showTooltip && (
                  <div className="absolute left-full ml-2 w-28 p-2 bg-gray-700 text-white text-xs rounded shadow-lg z-9999">
                    Only binary classification datasets with at least 20 samples and two features!
                    The first column must be named `Labels` and must contain exactly two unique values.
                  </div>
                )}
              </span>
            )}
          </li>
          {datasets.map((dataset, index) => (
            <li key={index} className="p-2 pl-8">
              {isOpen && (
                <span className="flex items-center">
                  <span className="block">{dataset}</span>
                </span>
              )}
            </li>
          ))}
          <li className="p-2 pl-8">
            <input
              type="file"
              accept=".csv"
              onChange={handleUpload}
              ref={fileInputRef}
              className="hidden"
              id="file-upload"
            />
            {uploadError && ( // Display error if it exists
              <div className="text-red-500 text-sm p-2">
                {uploadError}
              </div>
            )}
            {uploadMessage && ( // Display message if it exists
              <div className="text-green-500 text-sm p-2">
                {uploadMessage}
              </div>
            )}
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
