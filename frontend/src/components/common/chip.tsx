import React, { MouseEventHandler } from "react";

interface IProps {
  text: string;
  bgColor?: string;
  textColor?: string;
  bold?: boolean;
  btn?: boolean;
  onClick?: MouseEventHandler<HTMLButtonElement> | undefined;
}

export const Chip: React.FC<IProps> = ({
  text,
  textColor,
  bold,
  bgColor,
  btn,
  onClick,
}) => {
  return (
    <div
      className={`inline-flex items-center rounded-full border border-gray-200 px-1 py-1 ${bgColor}`}
    >
      <span
        className={`px-1 text-sm text-center w-full text-${textColor} ${bold ? "font-bold" : ""}`}
      >
        {text}
      </span>
      {btn ? (
        <button
          type="button"
          className="h-6 w-6 p-1 rounded-full bg-opacity-25 focus:outline-none"
          onClick={onClick}
        >
          <svg
            className="text-red-500 text-opacity-75"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </button>
      ) : null}
    </div>
  );
};
