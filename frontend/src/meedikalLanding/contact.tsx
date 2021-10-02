import React from "react";

interface IProps {}

const Contact: React.FC<IProps> = () => {
  return (
    <section className="text-gray-600 body-font lg:relative">
      <div className="hidden lg:absolute lg:flex lg:display-flex inset-0 bg-gray-300">
        <iframe
          className="border-0 focus:border-0 filter contrast-1 opacity-50"
          title="map"
          src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13095.168728844454!2d-56.1938193!3d-34.8614488!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa3c298c9fd703d35!2sSociedad%20M%C3%A9dica%20Universal!5e0!3m2!1sen!2suy!4v1633202238613!5m2!1sen!2suy"
          width="100%"
          height="100%"
        ></iframe>
      </div>
      <div className="container px-5 pt-0 py-6 lg:pt-8 lg:py-0 mx-auto flex">
        <div className="lg:w-1/3 md:w-1/2 bg-white rounded-lg p-8 flex flex-col md:ml-auto w-full mt-10 md:mt-0 relative z-10 shadow-lg">
          <p className="leading-relaxed mb-5 text-gray-600">
            Send feedback, comments, inquiries and suggestions to us:
          </p>
          <div className="relative mb-4">
            <label htmlFor="email" className="leading-7 text-sm text-gray-600">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
            />
          </div>
          <div className="relative mb-4">
            <label
              htmlFor="message"
              className="leading-7 text-sm text-gray-600"
            >
              Message
            </label>
            <textarea
              id="message"
              name="message"
              className="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out"
            ></textarea>
          </div>
          <button className="text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg">
            Send
          </button>
          <p className="text-xs text-gray-500 mt-3">
            We'll reach out as soon as possible.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
