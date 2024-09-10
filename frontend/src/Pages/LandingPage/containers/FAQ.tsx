import React, { useState } from 'react';

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  { question: 'Comment fonctionne votre service ?', answer: 'Notre service vous permet de... (détails sur le service).' },
  { question: 'Quels sont les tarifs ?', answer: 'Les tarifs varient en fonction... (détails sur les tarifs).' },
  { question: 'Puis-je annuler mon abonnement ?', answer: 'Oui, vous pouvez annuler à tout moment en... (détails sur l\'annulation).' },
];

const FAQ: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="max-w-2xl lg:max-w-4xl mx-auto p-8" id='FAQ'>
      {faqs.map((faq, index) => (
        <div key={index} className="mb-4">
          <div
            onClick={() => toggleFAQ(index)}
            className="flex justify-between items-center cursor-pointer text-gray-300 bg-gray-800 rounded-md p-4"
          >
            <h3 className="text-lg font-semibold">{faq.question}</h3>
            <svg
              className={`w-6 h-6 transition-transform transform ${openIndex === index ? 'rotate-180' : 'rotate-0'}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
          {openIndex === index && (
            <div className="mt-2 p-4 bg-gray-900 text-white rounded-md">
              <p>{faq.answer}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default FAQ;
