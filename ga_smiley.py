import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 28
rng = np.random.default_rng(42)


def hedef_olustur():
    """Çizimdeki gülen yüzü 28x28 matrise çevirir (1 = siyah çizgi, 0 = beyaz)."""
    img = np.zeros((N, N), dtype=np.uint8)
    yy, xx = np.mgrid[0:N, 0:N]
    # iki göz: halka + ortada nokta
    for cx, cy in [(9, 8), (19, 8)]:
        d = np.hypot(xx - cx, yy - cy)
        img[(d >= 2.0) & (d <= 3.0)] = 1
        img[d <= 0.8] = 1
    # kesik çizgili gülümseme (parabol)
    for x in range(6, 23, 2):
        y = int(round(18 - ((x - 14) / 8) ** 2 * 4))
        img[y, x] = 1
    return img


HEDEF = hedef_olustur().flatten()
L = HEDEF.size  # 784 gen


def uygunluk(pop):
    # doğru eşleşen piksel sayısı
    return (pop == HEDEF).sum(axis=1)


def evrimlestir(pop_size=200, nesil=2000, mut=1.0 / L, elit=2, turnuva=3):
    pop = rng.integers(0, 2, size=(pop_size, L), dtype=np.uint8)  # rastgele gürültü
    gecmis, anlik = [], {}
    for g in range(nesil + 1):
        fit = uygunluk(pop)
        en_iyi = fit.max()
        gecmis.append(en_iyi)
        if g in (0, 25, 50, 100, 200, 400) or en_iyi == L:
            anlik[g] = (pop[fit.argmax()].reshape(N, N).copy(), en_iyi)
        if en_iyi == L:
            break
        # elitizm
        sirali = np.argsort(fit)[::-1]
        yeni = [pop[i].copy() for i in sirali[:elit]]
        while len(yeni) < pop_size:
            # turnuva seçimi ile iki ebeveyn
            a = [max(rng.integers(0, pop_size, turnuva), key=lambda i: fit[i]) for _ in range(2)]
            p1, p2 = pop[a[0]], pop[a[1]]
            maske = rng.random(L) < 0.5  # uniform çaprazlama
            cocuk = np.where(maske, p1, p2)
            flip = rng.random(L) < mut  # mutasyon
            cocuk = np.where(flip, 1 - cocuk, cocuk).astype(np.uint8)
            yeni.append(cocuk)
        pop = np.array(yeni)
    return gecmis, anlik


if __name__ == "__main__":
    gecmis, anlik = evrimlestir()
    print(f"Son nesil: {len(gecmis) - 1}, en iyi uygunluk: {gecmis[-1]}/{L}")

    kareler = [("Hedef", HEDEF.reshape(N, N))] + [
        (f"Nesil {g}\n{f}/{L}", im) for g, (im, f) in sorted(anlik.items())
    ]
    fig, ax = plt.subplots(1, len(kareler), figsize=(2.2 * len(kareler), 2.8))
    for a, (baslik, im) in zip(np.atleast_1d(ax), kareler):
        a.imshow(1 - im, cmap="gray", vmin=0, vmax=1)
        a.set_title(baslik, fontsize=9)
        a.axis("off")
    plt.tight_layout()
    plt.savefig("evrim.png", dpi=130)

    plt.figure(figsize=(5, 3))
    plt.plot(gecmis)
    plt.xlabel("Nesil")
    plt.ylabel("En iyi uygunluk (doğru piksel)")
    plt.tight_layout()
    plt.savefig("uygunluk.png", dpi=130)
