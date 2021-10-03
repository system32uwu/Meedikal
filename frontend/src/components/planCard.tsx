import React from "react";

interface IProps {
  planName: string;
  price: number;
  popular: boolean;
  features: Array<string>;
  legendText: string;
}

const PlanCard: React.FC<IProps> = ({
  planName,
  price,
  popular,
  features,
  legendText,
}) => {
  return (
    <div className="p-4 xl:w-1/4 md:w-1/2 w-full">
      <div className="h-full p-6 rounded-lg border-2 border-turqoise flex flex-col relative overflow-hidden">
        {popular ? (
          <span className="bg-turqoise text-white px-3 py-1 tracking-widest text-xs absolute right-0 top-0 rounded-bl">
            POPULAR
          </span>
        ) : null}
        <h2 className="text-sm tracking-widest title-font mb-1 font-medium">
          {planName}
        </h2>
        <h1 className="text-5xl text-gray-900 pb-4 mb-4 border-b border-gray-200 leading-none">
          <span>${price}</span>
          <span className="text-lg ml-1 font-normal text-gray-500">/mo</span>
        </h1>
        {features.map((f) => (
          <p className="flex items-center text-gray-600 mb-2" key={f}>
            <span className="w-4 h-4 mr-2 inline-flex items-center justify-center bg-turqoise text-white rounded-full flex-shrink-0">
              <svg
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2.5"
                className="w-3 h-3"
                viewBox="0 0 24 24"
              >
                <path d="M20 6L9 17l-5-5"></path>
              </svg>
            </span>
            {f}
          </p>
        ))}
        <button className="flex items-center mt-auto text-white bg-turqoise border-0 py-2 px-4 w-full focus:outline-none hover:bg-gray-500 rounded">
          Learn More
          <svg
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            className="w-4 h-4 ml-auto"
            viewBox="0 0 24 24"
          >
            <path d="M5 12h14M12 5l7 7-7 7"></path>
          </svg>
        </button>
        <p className="text-xs text-gray-500 mt-3">{legendText}</p>
      </div>
    </div>
  );
};

export default PlanCard;
