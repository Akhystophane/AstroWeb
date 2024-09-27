import React, { useState } from 'react';

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  { question: 'Qui sommes nous 👀 ?', answer: "Notre équipe est composée d'astrologues, d'astronomes et de data analysts passionnés. Nous utilisons les données précises de la NASA pour calculer en temps réel la position des astres et leur influence. Grâce à notre puissant algorithme, nous sommes en mesure de générer des prédictions personnalisées et précises, adaptées à ton profil unique. C'est cette combinaison d'expertise humaine et technologique qui nous permet de te fournir des prévisions fiables sur différents aspects de ta vie." },
  { question: 'Est-ce gratuit ?', answer: "Pour le moment, tous les services de notre site sont 100% gratuits ! 🎉 C'est l'occasion idéale d'en profiter pleinement pour découvrir tes prédictions personnalisées sans aucun frais. Ne passe pas à côté de cette opportunité !" },
  { question: 'À quand de nouvelles fonctionnalités ?', answer: "Beaucoup de choses excitantes sont en préparation ! 🔥 Nous travaillons sur des tests de compatibilité amoureuse, un livret détaillé sur ta personnalité, et bien plus encore... Pour être parmi les premiers à les tester dès leur sortie, n'oublie pas de t'abonner à notre newsletter si ce n'est pas déjà fait. C'est le meilleur moyen de rester au courant des nouveautés !" },
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
