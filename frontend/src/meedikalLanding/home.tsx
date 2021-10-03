import React from "react";
import hero from "../static/hero.jpg";
import { Link } from "react-router-dom";

interface IProps {}

const Home: React.FC<IProps> = () => {
  return (
    <div>
      <section className="text-gray-600 body-font">
        <div className="container mx-auto flex px-5 py-8 md:flex-row flex-col items-center">
          <div className="lg:flex-grow md:w-1/2 lg:pr-24 md:pr-16 flex flex-col md:items-start md:text-left mb-16 md:mb-0 items-center text-center">
            <h1 className="title-font sm:text-4xl text-3xl mb-4 font-medium text-gray-900">
              Your health, <br />
              our priority
            </h1>
            <p className="mb-8 leading-relaxed">
              We're a widely known healthcare company, which has been offering
              high quality services and insurance to its users since 1910, we
              count with the most qualified medical personnel, the latest
              devices and the ideal plan for you and your family.
            </p>
            <div className="flex justify-center">
              <Link to="/plans">
                <button className="inline-flex text-white bg-turqoise border-0 py-2 px-6 focus:outline-none rounded text-lg">
                  Plans
                </button>
              </Link>
              <Link to="/contact">
                <button className="ml-4 inline-flex text-gray-700 bg-gray-100 border-0 py-2 px-6 focus:outline-none hover:bg-gray-200 rounded text-lg">
                  Contact
                </button>
              </Link>
            </div>
          </div>
          <div className="lg:max-w-lg lg:w-full md:w-1/2 w-5/6">
            <img
              className="object-cover object-center rounded"
              alt="hero"
              src={hero}
            />
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
