import React, { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';
import SolarSystemSVGPath from '../../../assets/SolarSystem.svg';

gsap.registerPlugin(MotionPathPlugin);

const convertCircleToPath = (circle: SVGCircleElement): SVGPathElement => {
  const cx = parseFloat(circle.getAttribute('cx')!);
  const cy = parseFloat(circle.getAttribute('cy')!);
  const r = parseFloat(circle.getAttribute('r')!);
  const pathData = `
    M ${cx - r}, ${cy}
    a ${r},${r} 0 1,0 ${r * 2},0
    a ${r},${r} 0 1,0 ${r * -2},0
  `;

  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', pathData);
  path.setAttribute('class', circle.getAttribute('class')!);
  path.setAttribute('id', circle.getAttribute('id')!);
  circle.replaceWith(path);
  return path;
};

const SolarSystemAnimation: React.FC = () => {
  const svgContainerRef = useRef<HTMLDivElement>(null);
  const circleRefs = useRef<SVGPathElement[]>([]);
  const planetRefs = useRef<SVGGElement[]>([]);
  const [svgContent, setSvgContent] = useState<string>('');


  useEffect(() => {
    fetch(SolarSystemSVGPath)
      .then((response) => response.text())
      .then((data) => {
        setSvgContent(data);
      })
      .catch((error) => console.error('Error loading SVG:', error));
  }, []);

  useEffect(() => {
    if (svgContent && svgContainerRef.current) {
      svgContainerRef.current.innerHTML = svgContent;
      const svgElement = svgContainerRef.current.querySelector('svg');
        

      if (svgElement) {

        const circles = [
          svgElement.getElementById('Circle1'),
          svgElement.getElementById('Circle2'),
          svgElement.getElementById('Circle3'),
          svgElement.getElementById('Circle4'),
          svgElement.getElementById('Circle5')
        ];

        const planets = [
          svgElement.getElementById('Mercury') as SVGGElement,
          svgElement.getElementById('Earth') as SVGGElement,
          svgElement.getElementById('Mars') as SVGGElement,
          svgElement.getElementById('Uranus') as SVGGElement,
          svgElement.getElementById('Jupiter') as SVGGElement
        ];

        const convertedCircles = circles.map((circle) => {
          if (circle instanceof SVGCircleElement) {
            return convertCircleToPath(circle);
          }
          return circle as SVGPathElement;
        });

        circleRefs.current = convertedCircles.filter(Boolean) as SVGPathElement[];
        planetRefs.current = planets.filter(Boolean) as SVGGElement[];

        gsap.to(planetRefs.current[0], {
          duration: 10,
          ease: 'linear',
          repeat: -1,
          motionPath: {
            path: circleRefs.current[0],
            align: circleRefs.current[0],
            alignOrigin: [0.5, 0.5]
          }
        });

        gsap.to(planetRefs.current[1], {
          duration: 15,
          ease: 'linear',
          repeat: -1,
          motionPath: {
            path: circleRefs.current[1],
            align: circleRefs.current[1],
            alignOrigin: [0.5, 0.5]
          }
        });

        gsap.to(planetRefs.current[2], {
          duration: 20,
          ease: 'linear',
          repeat: -1,
          motionPath: {
            path: circleRefs.current[2],
            align: circleRefs.current[2],
            alignOrigin: [0.5, 0.5]
          }
        });

        gsap.to(planetRefs.current[3], {
          duration: 25,
          ease: 'linear',
          repeat: -1,
          motionPath: {
            path: circleRefs.current[3],
            align: circleRefs.current[3],
            alignOrigin: [0.5, 0.5]
          }
        });

        gsap.to(planetRefs.current[4], {
          duration: 30,
          ease: 'linear',
          repeat: -1,
          motionPath: {
            path: circleRefs.current[4],
            align: circleRefs.current[4],
            alignOrigin: [0.5, 0.5]
          }
        });
      } else {
        console.error('SVG element not found');
      }
    }
  }, [svgContent]);

  return (
    <div className="h-full w-full flex justify-center items-center overflow-hidden relative">
      <div
        ref={svgContainerRef}
        className="absolute w-[80%] portrait:w-[220%]  h-full"
        style={{
          maskImage: 'linear-gradient(180deg, transparent 0%, black 30%, black 70%, transparent 100%)',
          WebkitMaskImage: 'linear-gradient(180deg, transparent 0%, black 30%, black 70%, transparent 100%)'
        }}
      >
        {/* Contenu du SVG */}
      </div>
 
    </div>
  );
};

export default SolarSystemAnimation;
