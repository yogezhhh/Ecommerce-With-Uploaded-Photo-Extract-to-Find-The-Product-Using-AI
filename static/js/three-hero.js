(function () {
  const canvas = document.getElementById('hero-3d');
  if (!canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const count = 1500;
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count * 3; i++) positions[i] = (Math.random() - 0.5) * 20;

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const particles = new THREE.Points(geo, new THREE.PointsMaterial({ size: 0.02, color: 0x7c3aed, transparent: true, opacity: 0.7 }));
  scene.add(particles);

  const knot = new THREE.Mesh(
    new THREE.TorusKnotGeometry(1.2, 0.35, 100, 16),
    new THREE.MeshBasicMaterial({ color: 0x06b6d4, wireframe: true, transparent: true, opacity: 0.4 })
  );
  knot.position.set(3, 1, -2);
  scene.add(knot);

  function animate() {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.0006;
    knot.rotation.x += 0.004;
    knot.rotation.y += 0.006;
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();