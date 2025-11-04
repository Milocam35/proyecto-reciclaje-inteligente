import React from "react";

const ChartCard = ({ title, children }) => {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-4 hover:scale-105 transition-transform duration-300 ease-in-out cursor-pointer">
      <h3 className="text-gray-700 font-semibold mb-3 text-sm">{title}</h3>
      <div className="h-40 flex justify-center items-center">{children}</div>
    </div>
  );
};

export default ChartCard;
