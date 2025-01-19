from immeuble import Immeuble
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from matplotlib.collections import PatchCollection
import matplotlib.animation as animation
import numpy as np
from matplotlib.animation import FuncAnimation
"""
##### PARAMETRES #####
masse_imm = 776e3     # Masse de l'immeuble en kg
masse_leste = 1824e3"""

masse_imm = 550e3
masse_leste = 1330e3
masse = masse_imm + masse_leste
#répartiton en 20 points
repartion_nu = np.array([0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05])
repartition_leste = np.array([0.7,0.3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
masse_imm_repartie = repartion_nu * masse_imm
masse_leste_repartie = repartition_leste * masse_leste

"""
L = 10          # Longueur de l'immeuble en mètres
l = 10          # Largeur de l'immeuble en mètres
H = 45          # Hauteur de l'immeuble en mètres
"""
l = 10
L = 10
H = 50
#####################################
########## INITIALISATION ###########
#####################################

#Arrow draw
def draw_self_loop_bas(center, radius, facecolor='#2693de', edgecolor='#000000', theta1=-30, theta2=180):
    
    # Add the ring
    rwidth = 1
    ring = mpatches.Wedge(center, radius, theta1, theta2, width=rwidth)
    # Triangle edges
    offset = 1
    xcent  = center[0] - radius + (rwidth/2)
    left   = [xcent - offset, center[1]]
    right  = [xcent + offset, center[1]]
    bottom = [(left[0]+right[0])/2., center[1]-2]
    arrow  = plt.Polygon([left, right, bottom, left])
    p = PatchCollection(
        [ring, arrow], 
        edgecolor = edgecolor, 
        facecolor = facecolor,
    )
    ax1.add_collection(p)

#Arrow draw
def draw_self_loop_haut(center, radius, facecolor='#2693de', edgecolor='#000000', theta1=-30, theta2=180):
    
    # Add the ring
    rwidth = 1
    ring = mpatches.Wedge(center, radius, theta1, theta2, width=rwidth)
    # Triangle edges
    offset = 1
    xcent  = center[0] - radius + (rwidth/2)
    left   = [xcent - offset, center[1]]
    right  = [xcent + offset, center[1]]
    bottom = [(left[0]+right[0])/2., center[1]+2]
    arrow  = plt.Polygon([left, right, bottom, left])
    p = PatchCollection(
        [ring, arrow], 
        edgecolor = edgecolor, 
        facecolor = facecolor,
    )
    ax1.add_collection(p)

#Ajoute un marqueur relatif au rectangle / réphérence au repère de l'immeuble à l'origine en bas à gauche
def convertisseur_rel_abs (coord):
    """ coord: (x,z) """
    x_absolu = immeuble_graph.get_corners()[0][0] + coord[0]*math.cos(immeuble_test.angle*math.pi/180) + coord[1]*math.sin(immeuble_test.angle*math.pi/180)
    z_absolu = immeuble_graph.get_corners()[0][1] + coord[1]*math.cos(immeuble_test.angle*math.pi/180) - coord[0]*math.sin(immeuble_test.angle*math.pi/180)

    return (x_absolu,z_absolu)
    
if __name__ =="__main__":

    angle_init = int(input("Définir un angle alpha: "))

    #Building INIT
    immeuble_test = Immeuble(angle=angle_init,
                            surface= L*l,
                            hauteur = H,
                            m_i_r = masse_imm_repartie,
                            m_l_r = masse_leste_repartie)

    immeuble_test.calcul_centre_masse()
    immeuble_test.calcul_centre_carene()

    immeuble_graph = mpatches.Rectangle((math.sqrt(immeuble_test.surface)/2 + 20, - immeuble_test.h_sub*math.cos(immeuble_test.angle*math.pi/180)),
                                math.sqrt(immeuble_test.surface),
                                    immeuble_test.hauteur,
                                    edgecolor = 'black',
                                    facecolor = 'beige',
                                    angle = -immeuble_test.angle,
                                    fill=True)

    #Recalcul data propre à l'immeuble
    x_cc,z_cc = convertisseur_rel_abs((immeuble_test.x_centre_carene,immeuble_test.z_centre_carene))
    x_cm,z_cm = convertisseur_rel_abs((immeuble_test.x_centre_masse,immeuble_test.z_centre_masse))
    x_geom,z_geom = immeuble_graph.get_center()

    #Init
    # Visualisation avec matplotlib
    fig, (ax1,ax2,ax3) = plt.subplots(1,3)
    # Ligne d'eau
    ax1.plot([0,100],[0,0])
    #Paramètrage plot
    ax1.set_ylim([-70,70])
    ax1.set_xlim([0,60])
    ax1.set_title(f"Position et moment à l'angle {angle_init}°")

    m_cc = ax1.plot(x_cc,z_cc, marker="x",label="Centre de carène")
    m_cm = ax1.plot(x_cm,z_cm,marker="x",label="Centre de masse")
    m_cg = ax1.plot(x_geom,z_geom,marker="x",label="Centre géométrique",color="black")
    
    ax1.legend()
    ax1.set_aspect('equal')
    ax1.set_xlabel("Coordonnée x en m")
    ax1.set_ylabel("Coordonnée z en m")

    rect_plt = ax1.add_patch(immeuble_graph)

    coins = immeuble_graph.get_corners()
    x_surface = np.concatenate((np.linspace(coins[3][0],coins[0][0],50),np.linspace(coins[0][0],coins[1][0],50),np.linspace(coins[1][0],coins[2][0],50)))
    y1_surface = [0 for i in range(150)]
    y2_surface = np.concatenate((np.linspace(coins[3][1],coins[0][1],50),np.linspace(coins[0][1],coins[1][1],50),np.linspace(coins[1][1],coins[2][1],50)))

    immeuble_test.fill = ax1.fill_between(x_surface,y1_surface, y2_surface, where=y2_surface <= y1_surface, color='skyblue', alpha=0.5, label='Area')
    

    if not immeuble_test.calcul_redressement(x_cm,x_cc):
        draw_self_loop_bas((x_cm,z_cm), 10, facecolor='#2693de', edgecolor='#000000', theta1=0, theta2=180)
    else:
        draw_self_loop_haut((x_cm,z_cm), 10, facecolor='#2693de', edgecolor='#000000', theta2=0, theta1=-180)
    """
    def update(frame):
        ##### Animation #####

        #MAJ Angle
        immeuble_graph.set_angle(-immeuble_test.angle)

        #Etude partie submergée
        coins = immeuble_graph.get_corners()
        x_surface = np.concatenate((np.linspace(coins[3][0],coins[0][0],50),np.linspace(coins[0][0],coins[1][0],50),np.linspace(coins[1][0],coins[2][0],50)))
        y1_surface = [0 for i in range(150)]
        y2_surface = np.concatenate((np.linspace(coins[3][1],coins[0][1],50),np.linspace(coins[0][1],coins[1][1],50),np.linspace(coins[1][1],coins[2][1],50)))

        immeuble_test.calcul_centre_carene()

        immeuble_test.fill.remove()
        immeuble_test.fill = ax.fill_between(x_surface,y1_surface, y2_surface, where=y2_surface <= y1_surface, color='skyblue', alpha=0.4, label='Area')
        
        #Recalcul data propre à l'immeuble
        x_cc,z_cc = convertisseur_rel_abs((immeuble_test.x_centre_carene,immeuble_test.z_centre_carene))
        x_cm,z_cm = convertisseur_rel_abs((immeuble_test.x_centre_masse,immeuble_test.z_centre_masse))
        x_geom,z_geom = immeuble_graph.get_center()
        x_trig,z_trig = convertisseur_rel_abs((immeuble_test.coord_x_triangle,immeuble_test.coord_z_triangle))

        immeuble_test.calcul_moment(x_cm,x_cc,z_cc)
        immeuble_test.calcul_acceleration_angulaire()

        #print(x_cc,x_cm)
        #MAJ des positions des markers
        m_cc[0].set_xdata([x_cc])
        m_cc[0].set_ydata([z_cc])

        m_cm[0].set_xdata([x_cm])
        m_cm[0].set_ydata([z_cm])

        m_cg[0].set_xdata([x_geom])
        m_cg[0].set_ydata([z_geom])
        
        immeuble_graph.set_y(- immeuble_test.h_sub)"""


    #####################################
    #### Plot 2 - repartition masse #####
    #####################################

    ax2.barh([-immeuble_test.h_sub + i*H/len(repartion_nu) for i in range(0,len(repartion_nu))],masse_imm_repartie, align='edge', height=0.7)
    ax2.barh([-immeuble_test.h_sub + i*H/len(repartition_leste) for i in range(0,len(repartition_leste))],masse_leste_repartie,left=masse_imm_repartie, align='edge', height=0.7)

    # Ajustements du graphique
    ax2.set_ylim(-immeuble_test.h_sub - 10, -immeuble_test.h_sub + H + 10)
    ax2.set_title(f" Répartition de la masse m_totale={"{:.2e}".format(masse)} kg ")
    ax2.set_xlabel('Masse (kgs)')
    ax2.set_ylabel(f"Tranches / étages")

    #####################################
    #### Plot 3 - évolution moments #####
    #####################################

    def convertisseur_rel_abs_temp (coord):
        """ coord: (x,z) """
        x_absolu = immeuble_graph_temp.get_corners()[0][0] + coord[0]*math.cos(immeuble_temp.angle*math.pi/180) + coord[1]*math.sin(immeuble_temp.angle*math.pi/180)
        z_absolu = immeuble_graph_temp.get_corners()[0][1] + coord[1]*math.cos(immeuble_temp.angle*math.pi/180) - coord[0]*math.sin(immeuble_temp.angle*math.pi/180)

        return (x_absolu,z_absolu)
    
    evolution_moments = []
    for angle_temp in range(-80,88,8):
        #Génère des cas et calcul les moments associés
        immeuble_temp = Immeuble(angle=angle_temp,
                            surface= L*l,
                            hauteur = H,
                            m_i_r = masse_imm_repartie,
                            m_l_r = masse_leste_repartie)
        
        immeuble_temp.calcul_centre_masse()
        immeuble_temp.calcul_centre_carene()

        immeuble_graph_temp = mpatches.Rectangle((math.sqrt(immeuble_temp.surface)/2 + 20, - immeuble_temp.h_sub*math.cos(immeuble_temp.angle*math.pi/180)),
                                math.sqrt(immeuble_temp.surface),
                                    immeuble_temp.hauteur,
                                    edgecolor = 'black',
                                    facecolor = 'beige',
                                    angle = -immeuble_temp.angle,
                                    fill=True)
        
        
        print(immeuble_temp.z_centre_carene,immeuble_temp.z_centre_masse)
        #Recalcul data propre à l'immeuble
        x_cc_temp,z_cc_temp = convertisseur_rel_abs_temp((immeuble_temp.x_centre_carene,immeuble_temp.z_centre_carene))
        x_cm_temp,z_cm_temp = convertisseur_rel_abs_temp((immeuble_temp.x_centre_masse,immeuble_temp.z_centre_masse))
        immeuble_temp.calcul_moment(x_cm_temp,x_cc_temp,z_cc_temp)
        evolution_moments.append(int(immeuble_temp.moment_cinetique))
        print(evolution_moments)
        print("Angle: ", angle_temp, "/ Moment:", immeuble_temp.moment_cinetique)

    ax3.hlines(y=0,xmin=-90,xmax=90, color='r', linestyle='--')
    ax3.plot(np.linspace(-80,80,21),evolution_moments)
    ax3.set_xlabel("angle en degrés")
    ax3.set_ylabel("Moment subit par l'immeuble")
    ax3.set_title("Moment selon différents angles")
    plt.show()