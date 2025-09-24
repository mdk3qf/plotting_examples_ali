import numpy as np
import matplotlib.pyplot as plt

def myplots(samples=10000):
    # to create canvas1_py.png
    mu = 100
    sigma = 6
    data1 = np.random.normal(mu, sigma, samples)

    # have to handle errors manually
    counts1, bins1 = np.histogram(data1, bins=100, range=(50, 150))
    bin_centers1 = 0.5*(bins1[:-1]+bins1[1:])
    errors1 = np.sqrt(counts1)

    fig1, ax1 = plt.subplots()

    ax1.hist(data1, bins=100, range=(50, 150), linewidth=0.75, histtype="step", label="Mean    100 \nStd Dev    6")
    ax1.errorbar(bin_centers1, counts1, yerr=errors1, linestyle="None", linewidth=0.75, color="#1f77b4")
    ax1.set_title("Random Gauss")
    ax1.set_xlabel("x")
    ax1.set_ylabel("Frequency")
    ax1.legend()
    fig1.tight_layout()
    fig1.savefig("canvas1_py.png", dpi=300)


    # to create canvas2_py.png
    fig2, axes = plt.subplots(2, 2, figsize=(8, 6))


    # 1: Gaussian
    axes[0,0].hist(data1, bins=100, range=(50, 150), linewidth=0.75, histtype="step", label="Mean    100 \nStd Dev    6")
    axes[0,0].errorbar(bin_centers1, counts1, yerr=errors1, linestyle="None", linewidth=0.75, color="#1f77b4")
    axes[0,0].set_title("Random Gauss")
    axes[0,0].set_xlabel("x")


    # 2: Gaussian + uniform offset
    # floored division of sample size defines offset
    data2 = np.concatenate([data1, np.random.uniform(50, 150, samples // 3)])

    counts2, bins2 = np.histogram(data2, bins=100, range=(50, 150))
    bin_centers2 = 0.5*(bins2[:-1]+bins2[1:])
    errors2 = np.sqrt(counts2)

    axes[0,1].errorbar(bin_centers2, counts2, yerr=errors2, linestyle="None", linewidth=0.75, color="#1f77b4")
    axes[0,1].hist(data2, bins=100, range=(50, 150), linewidth=0.75, histtype="step")
    axes[0,1].set_title("Gauss + offset")
    axes[0,1].set_xlabel("x")


    # 3: Gaussian + 1/x^2 offset
    x = np.linspace(1, 11, samples*30)
    # sample with PDF proportional to 1/x^2
    prob = 1/x**2
    prob /= prob.sum()
    sampled = np.random.choice(x, size=samples*30, p=prob)
    data3 = np.concatenate([data1, sampled*10+40])

    counts3, bins3 = np.histogram(data3, bins=100, range=(50, 150))
    bin_centers3 = 0.5*(bins3[:-1]+bins3[1:])
    errors3 = np.sqrt(counts3)

    axes[1,0].errorbar(bin_centers3, counts3, yerr=errors3, linestyle="None", linewidth=0.75, color="#1f77b4")
    axes[1,0].hist(data3, bins=100, range=(50, 150), linewidth=0.75, histtype="step")
    axes[1,0].set_title("Gauss + offset2")
    axes[1,0].set_xlabel("x")
    axes[1,0].set_yscale("log")


    # 4: Double Gaussian
    data4 = np.concatenate([data1, np.random.normal(mu, 20, samples//2)])
    
    counts4, bins4 = np.histogram(data4, bins=100, range=(50, 150))
    bin_centers4 = 0.5*(bins4[:-1]+bins4[1:])
    errors4 = np.sqrt(counts4)

    axes[1,1].errorbar(bin_centers4, counts4, yerr=errors4, linestyle="None", linewidth=0.75, color="#1f77b4")
    axes[1,1].hist(data4, bins=100, range=(50, 150), linewidth=0.75, histtype="step")
    axes[1,1].set_title("Double Gaussian")
    axes[1,1].set_xlabel("x")


    fig2.tight_layout()
    fig2.savefig("canvas2_py.pdf")


if __name__ == "__main__":
    myplots()
