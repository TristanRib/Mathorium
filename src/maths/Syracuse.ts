import {MathHelper} from "../helpers/MathHelper";

/**
 * Hypothèse mathématique selon laquelle la suite de Syracuse de n'importe quel entier strictement positif atteint 1.
 */
export class Syracuse {
    private suite: number[] = [];

    constructor(private readonly number: number) {
    }

    private _recursive(n: number): void {
        this.suite.push(n);
        if (n > 1) {
            this._recursive(n % 2 === 0 ? n / 2 : n * 3 + 1);
        }
    }

    generateSuite(): number[] {
        this.suite = [];
        this._recursive(this.number);
        return this.suite;
    }

    get flyTime(): number {
        return this.suite.length - 1;
    }

    get altFlyTime(): number {
        const index = this.suite.findIndex((val) => val < this.number)
        return index !== -1 ? index : this.flyTime;
    }

    get maxAlt(): number {
        return Math.max(...this.suite);
    }
}

export function evaluateSyracuse(n: number) {
    const instances = new Map<number, { flyTime: number; altFlyTime: number; maxAlt: number }>();

    MathHelper.generateRange(n).forEach((num) => {
        const syracuse = new Syracuse(num);
        syracuse.generateSuite();

        instances.set(num, {
            flyTime: syracuse.flyTime,
            altFlyTime: syracuse.altFlyTime,
            maxAlt: syracuse.maxAlt,
        });
    });

    return new Map([...instances].sort((a, b) => b[1].flyTime - a[1].flyTime));
}