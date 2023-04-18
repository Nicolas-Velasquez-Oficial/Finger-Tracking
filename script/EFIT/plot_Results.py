import numpy as np
import matplotlib.pyplot as plt

def plot_Results(x, y, res, pars, subj, names, time):

    # Computing useful graphic parameters
    angleX = np.vectorize(lambda x1, x2: np.arctan2(x2, x1) * 180 / np.pi)
    xC2 = np.linspace(angleX(pars['d'][0], pars['d'][1]), angleX(pars['a'][0], pars['a'][1]), 100)
    xC1 = np.linspace(angleX(-pars['b'][0], pars['b'][1]), angleX(-pars['c'][0], pars['c'][1]), 100)
    rescaled_xC2 = np.mod(xC2 + (360 - 180), 360)
    rescaled_xC1 = np.mod(xC1 + (360 - 180), 360)
    pols_xC1_rad = np.deg2rad(rescaled_xC1)
    pols_xC2_rad = np.deg2rad(rescaled_xC2)
    radians_lbls = [pols_xC1_rad[0], pols_xC2_rad[-1]]
    radians_lbls2 = np.concatenate((pols_xC1_rad, pols_xC2_rad))
    k = np.where(res['xHist'] == np.median(res['xHist']))[0][0]
    xHist_zeta1 = res['xHist'][:k]
    xHist_zeta2 = res['xHist'][k+1:]

    # Create figure
    plt.close('all')
    fig = plt.figure(figsize=(17, 8.5), dpi=80)
    fig.canvas.set_window_title('EMOT analysis')

    # Empirical mouse-movements
    ax1 = plt.subplot(3, 7, (1, 10))
    ax1.add_patch(plt.Rectangle((pars['c'][0], pars['c'][1]), abs(pars['c'][0] - pars['b'][0]), abs(pars['d'][1] - pars['c'][1]), linewidth=1, linestyle='--', facecolor='white'))
    ax1.add_patch(plt.Rectangle((-pars['b'][0], pars['b'][1]), abs(pars['c'][0] - pars['b'][0]), abs(pars['d'][1] - pars['c'][1]), linewidth=1, linestyle='--', facecolor='white'))
    ax1.text(pars['b'][0] - 0.1, pars['d'][1] + 0.05, 'C2', color='black', fontsize=14, fontname='Arial')
    ax1.text(-pars['b'][0], pars['d'][1] + 0.05, 'C1', color='black', fontsize=14, fontname='Arial')
    ax1.text(pars['c'][0] + 0.05, pars['d'][1] / 1.15, names[0].upper(), color='black', fontsize=17, fontname='Arial')
    ax1.text(-pars['b'][0] + 0.05, pars['d'][1] / 1.15, names[1].upper(), color='black', fontsize=17, fontname='Arial')
    ax1.text(x[0] - 0.17, y[0] - 0.17, names[2].upper(), color='black', fontsize=17, fontname='Arial')
    ax1.set_xlim([-pars['b'][0] - 0.3, pars['b'][0] + 0.3])
    ax1.set_ylim([0, pars['d'][1] + 0.2])
    ax1.scatter(x, y, color='b')
    ax1.plot(np.linspace(-2, 2, 200), res['thr'])
    ax1.set_title(f'Participant ID: {subj}', fontsize=18, fontweight='bold', fontname='Arial')

    # Histogram H_theta and H_theta0
    ax2 = plt.subplot(3, 7, (4, 13))
    ax2.bar(res['xHist'], res['H_theta'] / np.sum(res['H_theta']), color=[0.6, 0.6, 0.6])
    ax2.bar(res['xHist'], (res['H_theta0'] / np.sum(res['H_theta0']) + 1e-19), color=[0.9, 0.9, 0.9])
    ax2.set_xlim([np.min(res['xHist']) - 0.20, np.max(res['xHist']) + 0.20])
    ax2.plot(radians_lbls2, np.zeros_like(radians_lbls2), '-ks', markersize=2, color=[0.05, 0.05, 0.05])
    ax2.text(np.mean(radians_lbls2[:len(radians_lbls2)//2]), -0.028, 'C1', color='black', fontsize=14, fontname='Arial')
    ax2.text(np.mean(radians_lbls2[len(radians_lbls2)//2:]), -0.028, 'C2', color='black', fontsize=14, fontname='Arial')
    ax2.legend(['H_theta', 'H_theta0'], fontsize=15, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
    ax2.get_legend().set_title(None)

    # Histograms CSI
    ax3 = plt.subplot(3, 7, (25, 26))
    ax3.bar(res['xHist'], res['tau'], color=[0.9, 0.9, 0.9])
    ax3.legend(['tau'], fontsize=15, loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=1)
    ax3.get_legend().set_title(None)
    ax3.set_xlim([np.min(res['xHist']) - 0.20, np.max(res['xHist']) + 0.20])

    # Histograms ZETA1 e ZETA2
    ax4 = plt.subplot(3, 7, (27, 28))
    ax4.bar(xHist_zeta1, res['u1'], color=[0.9, 0.9, 0.9])
    ax4.bar(xHist_zeta2, res['u2'], color=[0.6, 0.6, 0.6])
    ax4.legend(['upsilon_1', 'upsilon_2'], fontsize=14, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
    ax4.get_legend().set_title(None)
    ax4.set_xlim([np.min(xHist_zeta1) - 0.20, np.max(xHist_zeta2) + 0.20])

    # Text of results
    fontText = 16
    ax5 = plt.subplot(3, 7, 15)
    ax5.text(0, 0.8, f'psi = {res["psi"]}', color='black', fontsize=fontText, fontname='Arial')
    ax5.text(1.4, 0.8, f'xi = {res["csi"]}', color='black', fontsize=fontText, fontname='Arial')
    ax5.text(0, 0.6, f'zeta = {res["zeta"]}', color='black', fontsize=fontText, fontname='Arial')
    ax5.text(1.4, 0.55, f'zeta_1 = {res["zeta1"]}', color='black', fontsize=fontText, fontname='Arial')
    ax5.text(0, 0.35, f'zeta_2 = {res["zeta2"]}', color='black', fontsize=fontText, fontname='Arial')
    ax5.text(1.4, 0.4, f't = {time[0]} ({time[1]}) ms', color='black', fontsize=fontText, fontname='Arial')
    ax5.axis('off')

    plt.tight_layout()
    plt.show()