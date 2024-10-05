const Footer = () => {
    const apiUrl = process.env.NODE_ENV === 'production' ? '/newsletter/' : 'http://localhost:8000/newsletter/';


  return (
    
<div className="flex justify-center items-center p-10">
  <a 
    href={apiUrl} // Assure-toi que apiUrl est défini en amont dans ton code
    className="relative bg-gradient-to-br from-purple-600 to-indigo-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-gray-600 focus:outline-none"
  >
    <span className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 rounded-lg"></span>
    <span className="relative z-0">👉 Newsletter 👈</span>
  </a>
</div>

  )
}

export default Footer