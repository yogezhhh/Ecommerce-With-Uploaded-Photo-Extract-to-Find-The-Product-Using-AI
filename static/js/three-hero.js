(function () {
  const canvas = document.getElementById('hero-3d');
  if (!canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
  camera.position.z = 5;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));

  const count = 1500;
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count * 3; i++) positions[i] = (Math.random() - 0.5) * 20;

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const particles = new THREE.Points(geo, new THREE.PointsMaterial({ size: 0.02, color: 0x7c3aed, transparent: true, opacity: 0.7 }));
  scene.add(particles);

  const knot = new THREE.Mesh(
    new THREE.TorusKnotGeometry(1.2, 0.35, 120, 16),
    new THREE.MeshBasicMaterial({ color: 0x06b6d4, wireframe: true, transparent: true, opacity: 0.35 })
  );
  knot.position.set(3, 1, -2);
  scene.add(knot);

  const ico = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.9, 0),
    new THREE.MeshBasicMaterial({ color: 0x7c3aed, wireframe: true, transparent: true, opacity: 0.5 })
  );
  ico.position.set(-3.5, -1, -1);
  scene.add(ico);

  const mouse = { x: 0, y: 0 };
  window.addEventListener('mousemove', e => {
    mouse.x = (e.clientX / innerWidth - 0.5) * 2;
    mouse.y = (e.clientY / innerHeight - 0.5) * 2;
  });

  (function animate() {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.0006;
    knot.rotation.x += 0.004; knot.rotation.y += 0.006;
    ico.rotation.x -= 0.003; ico.rotation.y -= 0.005;
    camera.position.x += (mouse.x * 0.6 - camera.position.x) * 0.05;
    camera.position.y += (-mouse.y * 0.6 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);
    renderer.render(scene, camera);
  })();

  window.addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  });
})();