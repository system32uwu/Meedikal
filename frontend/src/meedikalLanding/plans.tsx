import React from "react";
import PlanCard from "../components/planCard";

interface IProps {}

const featureX = (x: number) => {
  let lst = Array(x);
  for (let i = 1; i <= x; i++) lst.push(`feature ${i}`);
  return lst;
};

const plans = [
  {
    planName: "Plan 1",
    price: 100,
    popular: false,
    features: featureX(3),
    legendText: "Aliqua in ullamco qui ullamco velit amet.",
  },
  {
    planName: "Plan 2",
    price: 190,
    popular: true,
    features: featureX(5),
    legendText:
      "Quis deserunt qui sunt aliquip culpa qui ipsum amet sint fugiat.",
  },
  {
    planName: "Plan 3",
    price: 400,
    popular: false,
    features: featureX(6),
    legendText: "Eu ad culpa ipsum pariatur dolore eiusmod ullamco sunt.",
  },
  {
    planName: "Plan 4",
    price: 750,
    popular: false,
    features: featureX(6),
    legendText: "Commodo labore duis eu reprehenderit ipsum voluptate.",
  },
];

const Plans: React.FC<IProps> = ({}) => {
  return (
    <section className="text-gray-600 body-font overflow-hidden">
      <div className="container px-5 py-4 mx-auto">
        <div className="flex flex-col text-center w-full mb-2">
          <h1 className="sm:text-4xl text-3xl font-medium title-font mb-2 text-gray-900">
            Plans
          </h1>
          <p className="lg:w-2/3 mx-auto leading-relaxed text-base text-gray-500">
            Choose the ideal plan for yourself and your loved ones.
          </p>
        </div>
        <div className="flex flex-wrap px-4">
          {plans.map((p) => (
            <PlanCard {...p} key={p.planName} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Plans;
