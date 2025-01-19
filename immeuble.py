import math

G = 9.81
RHO_EAU = 1020
CX = 2

class Immeuble():
    def __init__(self,m_i_r,m_l_r,hauteur, surface = 100, angle = 0):
        self.angle = angle
        self.hauteur = hauteur
        self.surface = surface
        self.largeur = math.sqrt(self.surface)
        self.vitesse_angulaire = 0
        self.fill = 0
        self.repartiton_m_tot = m_i_r+m_l_r
        self.masse = sum(self.repartiton_m_tot)

    def __str__(self):
        return f"\nImmeuble de {self.nb_etages} étages\n"
    
    def calcul_centre_masse(self):
        somme = 0
        nb_etages = len(self.repartiton_m_tot)
        demi_hauteur = (self.hauteur/nb_etages)/ 2
        for i in range(0,nb_etages):
            somme += self.repartiton_m_tot[i] * ((i*2*+1)*demi_hauteur)
        self.z_centre_masse = somme/self.masse
        self.x_centre_masse = self.largeur/2

    def calcul_centre_carene(self):
        self.v_sub_total = self.masse / RHO_EAU

        hauteur_triangle = self.largeur*math.tan(self.angle*math.pi/180)
        v_triangle = 0.5 * hauteur_triangle*self.surface
        v_carre = self.v_sub_total - v_triangle

        self.h_sub = v_carre/self.surface

        # Estimation de la position du centre de carene
        self.coord_x_triangle = self.largeur*2/3
        self.coord_z_triangle = self.h_sub + self.largeur*math.tan(self.angle*math.pi/180)*1/3
        self.x_centre_carene = ((self.largeur/2) * v_carre + (self.largeur*2/3)*v_triangle) / self.v_sub_total
        self.z_centre_carene = ((self.h_sub/2) * v_carre + (self.h_sub + self.largeur*math.tan(self.angle*math.pi/180)*1/3)*v_triangle) / self.v_sub_total


    def calcul_redressement(self,x_cm_abs,x_cc_abs):
        """
        Return True si moment de redressement sinon false
        """
        #Forces sont censé avoir la meme norme
        f_masse = - self.masse * G
        f_archimede = self.v_sub_total * RHO_EAU * G
        m_masse = f_masse * (x_cc_abs - x_cm_abs) # ajout d'un moins car on veut la norme
        self.moment_cinetique = m_masse
        return m_masse > 0
    
    def calcul_moment(self,x_cm_abs,x_cc_abs,z_cc_abs):
        #Moment cinetique non calculé précisément -- WORK IN PROGRESS / on retourne que le moment de la masse actuellement
        f_masse = - self.masse * G
        #f_trainee_discret = [0.5 * RHO_EAU * self.h_sub * self.largeur * CX * ((i+1)*self.vitesse_angulaire)**2 for i in range(round(self.h_sub))]
        m_trainee = 0

        #for i in range(len(f_trainee_discret)):
        #    m_trainee += f_trainee_discret[i] * ((i+1) - z_cc_abs) 
        m_masse = f_masse * (x_cc_abs - x_cm_abs) # ajout d'un moins car on veut la norme
        self.moment_cinetique = m_masse
        return m_masse
    
    def calcul_acceleration_angulaire(self):
        self.moment_inertie = (self.masse / 12)*(self.largeur**2 + self.hauteur**2)
        self.acceleration_angulaire = self.moment_cinetique / self.moment_inertie
        #print(self.vitesse_angulaire)
        return self.acceleration_angulaire

if __name__ == "__main__":
    immeuble1 = Immeuble(nb_etages=5)
    print(immeuble1)