import React from "react";

interface IProps {}

const Contact: React.FC<IProps> = () => {
  return (
    <section className="text-gray-600 body-font relative">
      <div className="container px-5 py-4 mx-auto flex sm:flex-nowrap flex-wrap">
        <div className="lg:w-2/3 md:w-1/2 bg-gray-300 rounded-lg overflow-hidden sm:mr-10 p-10 flex items-end justify-start relative">
          <iframe
            className="border-0 focus:border-0 filter contrast-1 opacity-50 absolute inset-0"
            title="map"
            src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13095.168728844454!2d-56.1938193!3d-34.8614488!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xa3c298c9fd703d35!2sSociedad%20M%C3%A9dica%20Universal!5e0!3m2!1sen!2suy!4v1633202238613!5m2!1sen!2suy"
            width="100%"
            height="100%"
          />
          <div className="bg-white relative flex flex-wrap py-6 rounded shadow-md lg:ml-8">
            <div className="lg:w-1/2 px-6">
              <h2 className="title-font font-semibold text-gray-900 tracking-widest text-xs">
                ADDRESS
              </h2>
              <p className="mt-1">Jorge Canning 2363, Montevideo</p>
            </div>
            <div className="lg:w-1/2 px-6 mt-4 lg:mt-0">
              <h2 className="title-font font-semibold text-gray-900 tracking-widest text-xs">
                EMAIL
              </h2>
              <a className="text-turqoise leading-relaxed">
                support@hccompay.com
              </a>
              <h2 className="title-font font-semibold text-gray-900 tracking-widest text-xs mt-4">
                PHONE
              </h2>
              <p className="leading-relaxed">123-456-7890</p>
            </div>
          </div>
        </div>
        <div className="lg:w-1/3 md:w-1/2 bg-white flex flex-col md:ml-auto w-full py-2 md:mt-0">
          <h2 className="text-gray-900 text-lg mb-1 font-medium title-font">
            Feedback
          </h2>
          <p className="leading-relaxed text-sm mb-2 text-gray-600">
            Let us know about your feedback, comments, inquiries and suggestions
          </p>
          <div className="relative mb-4">
            <label htmlFor="email" className="leading-7 text-sm text-gray-600">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="w-full bg-white rounded border border-gray-300 focus:border-turqoise focus:ring-2 focus:ring-turqoise text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
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
              className="w-full bg-white rounded border border-gray-300 focus:border-turqoise focus:ring-2 focus:ring-turqoise h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out"
            ></textarea>
          </div>
          <button className="text-white bg-turqoise border-0 py-2 px-6 focus:outline-none rounded text-lg">
            Send
          </button>
          <p className="text-xs text-gray-500 mt-3">
            We'll reach out as soon as possible. Your information will not be disclosed.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
