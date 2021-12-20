import {vec3} from 'gl-matrix';
class Particle {
    mp: vec3;
    p: vec3;
    v: vec3;
    pBest: vec3;
    fBest: number;

    constructor(p: vec3) {
        this.p = p;
        this.v = vec3.fromValues(
        (Math.random() - 0.5) / 2,
        (Math.random() - 0.5) / 2,
        (Math.random() - 0.5) / 2);
        this.pBest = vec3.fromValues(0, 0, 0);
        this.fBest = -99999999;
    }
}

function sm(c: number, v: vec3) {
    return vec3.fromValues(c * v[0], c * v[1], c * v[2]);
}

function add(v1: vec3, v2: vec3) {
    return vec3.fromValues(v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]);
}

function sub(v1: vec3, v2: vec3) {
    return vec3.fromValues(v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]);
}

class ParticleSwarmCloud {
    neighborhoods: Map<string, [number, vec3]>;
    particles: Array<Particle>;
    fitness: Function;
    nhSize: number;

    w: number;
    c1: number;
    c2: number;

    constructor(n: number, nhSize: number, fitness: Function) {
        this.particles = new Array<Particle>();
        this.fitness = fitness;
        for (let i = 0; i < n; i++) {
            let particle = new Particle(
                vec3.fromValues(
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2
            ));

            particle.pBest = particle.p;
            particle.mp = particle.p;
            particle.fBest = this.fitness(particle.p, particle.mp);

            this.particles.push(particle);
        }

        this.nhSize = nhSize;
        this.w = 0.4;
        this.c1 = 0.3;
        this.c2 = 0.3;
        this.calcNeighborhoods();
    }

    calcNeighborhoods() {
        this.neighborhoods = new Map<string, [number, vec3]>();
        for (let i = 0; i < this.particles.length; i++) {
            let particle = this.particles[i];
            let nx = Math.floor(particle.p[0] / this.nhSize);
            let ny = Math.floor(particle.p[1] / this.nhSize);
            let nz = Math.floor(particle.p[2] / this.nhSize);
            let coords:string = [nx, ny, nz].join(',');

            if (this.neighborhoods.has(coords)) {
                let old = this.neighborhoods.get(coords);
                if (old[0] < particle.fBest) {
                    this.neighborhoods.set(coords, [particle.fBest, particle.pBest]);
                }
            } else {
                this.neighborhoods.set(coords, [particle.fBest, particle.pBest]);
            }
        }
    }

    stepParticles() {
        for (let i = 0; i < this.particles.length; i++) {
            let part = this.particles[i];
            let inertial = sm(this.w, part.v);

            let r1 = Math.random();
            let r2 = Math.random();
            let pd = sm(this.c1 * r1, sub(part.pBest, part.p));

            let nx = Math.floor(part.p[0] / this.nhSize);
            let ny = Math.floor(part.p[1] / this.nhSize);
            let nz = Math.floor(part.p[2] / this.nhSize);
            let gBest = this.neighborhoods.get([nx, ny, nz].join(','))[1];
            let gd = sm(this.c2 * r2, sub(gBest, part.p));
            let tv = add(inertial, add(pd, gd))
            let len = vec3.length(tv);
            part.v = len == 0 ? part.v : sm(1/len, tv);
            let ll = vec3.length(part.v);
            if (len == 0) {
                console.log('ohhh');
            }
            part.p = add(sm(0.01, part.v), part.p);
            let f = this.fitness(part.p, part.mp);
            if (f >= part.fBest) {
                part.fBest = f;
                part.pBest = part.p;
            }

            part.mp = add(sm(0.001, part.p), sm(0.999, part.mp));
        }

        this.calcNeighborhoods();
    }
}

export default ParticleSwarmCloud;