import HeroSection from './containers/HeroSection'
import BirthChartSection from './containers/BirthChartSection'
import HoroscopeSection from './containers/HoroscopeSection'
import FAQ from './containers/FAQ'
import StarsBackground from '../../assets/StarsBackground.svg'
import Footer from './containers/Footer'






function App() {

  return (
    <>
      <div className='h-full w-full' style={{ backgroundImage: `url(${StarsBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
        < HeroSection  />
        < BirthChartSection />
        < HoroscopeSection />
        < FAQ/>
        < Footer />
      </div>

    </>
  )
}

export default App
