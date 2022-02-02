class Parser:



    # Parser header
    def __init__(self, lexer):
        self.next_token = lexer.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token type " + self.token.type + ". Expected: " + token_type)
        if token_type != 'EOF':
            self.token = self.next_token()

    def error(self, msg):
        raise RuntimeError('Parser error, %s' % msg + " on line " +
     str(self.token.line) + " column " + str(self.token.column) + ". Current value " 
     + "\"" + str(self.token.value) + "\"" + " type " + str(self.token.type))

    # Parser body

    def start(self):
        # start -> program EOF
        if self.token.type == 'EOF' or self.token.type == 'volumes' or self.token.type == 'services' or self.token.type == 'version' or self.token.type == 'networks':
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        # program -> newline program
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.program()
        # program -> top_level_element program
        elif self.token.type == 'volumes' or self.token.type == 'services' or self.token.type == 'version' or self.token.type == 'networks':
            self.top_level_element()
            self.program()
        else:
            pass

    def top_level_element(self):
        # top_level_element -> version assign ID NEWLINE top_level_element
        if self.token.type == 'version':
            self.take_token('version')
            self.take_token('ASSIGN')
            self.take_token('ID')
            self.take_token('NEWLINE')
            self.top_level_element()
            print("top level element OK")
        # top_level_element -> services assign newline indentation indentation services_element
        elif self.token.type == 'services':
            self.take_token('services')
            self.take_token('ASSIGN')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.services_element()
        elif self.token.type == 'volumes':
            self.take_token('volumes')
            self.take_token('ASSIGN')
            self.top_level_inner_element()
        elif self.token.type == 'networks':
            self.take_token('networks')
            self.take_token('ASSIGN')
            self.top_level_inner_element()
        elif self.token.type == 'EOF':
            self.take_token('EOF')
    
    def top_level_inner_element(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('ID')
                self.take_token('ASSIGN')
                self.top_level_inner_element()
            else:
                self.top_level_inner_element()
                self.top_level_element()
        

    def version(self):
        pass

    def assign_prod(self):
        pass

    def services_element(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
        # services_element -> ID assign newline image_prod
        if self.token.type == 'image':
            self.image_prod()
        # services_element -> ID assign newline build
        elif self.token.type == 'build':
            self.build_prod()
        # services_element -> ID assign newline ports
        elif self.token.type == 'ports':
            self.ports_prod()
        # services_element -> ID assign newline networks
        elif self.token.type == 'networks':
            self.networks_prod()
        # services_element -> ID assign newline deploy
        elif self.token.type == 'deploy':
            self.deploy_prod()
        elif self.token.type == 'volumes':
            self.volumes_prod()
        elif self.token.type == 'EOF':
            self.take_token('EOF')
        else:
            self.error("Only image, build, ports, networks, deploy allowed when defining services element")

    def image_prod(self):
        self.take_token('image')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.take_token('ID')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
            self.services_element()
        elif self.token.type == 'NEWLINE':
            self.take_token('ASSIGN')
            self.take_token('INDENTATION')
            self.top_level_element()
        else:
            self.error("ASSIGN required")

    def build_prod(self):
        self.take_token('build')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.take_token('ID')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.services_element()
        elif self.token.type == 'NEWLINE':
            self.take_token('ASSIGN')
            self.take_token('INDENTATION')
            self.top_level_element()
        else:
            self.error("build keyword required")
            

    def ports_prod(self):
        self.take_token('ports')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.list_member_prod()
        else:
            self.error("port keyword required")

    def list_member_prod(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.take_token('LIST_INDICATOR')
                self.take_token('ID')
            self.skip_prod()
            self.services_element()
            self.top_level_element()
        else:
            self.error("NEWLINE required for list member")

    def skip_prod(self):
        if self.token.type == "SPACE":
            self.take_token('SPACE')
            self.skip_prod()
        if self.token.type == 'INDENTATION':
            self.take_token('INDENTATION')
            self.skip_prod()
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.skip_prod()


    def networks_prod(self):
        self.take_token('networks')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.list_member_prod()
        else:
            self.error("ASSIGN required after networks")

    def volumes_prod(self):
        self.take_token('volumes')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.list_member_prod()
        else:
            self.error("ASSIGN required after volumes")



    def deploy_prod(self):
        self.take_token('deploy')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
            self.deploy_element()
        else:
            self.error("ASSIGN required after deploy")

    def deploy_element(self):

        if self.token.type == 'ID':
            self.take_token('ID')
            if self.token.type == 'ASSIGN':
                self.take_token('ASSIGN')
                self.take_token('ID')
                self.deploy_element()
        elif self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.deploy_element()
            else:
                self.skip_prod()
                self.top_level_element()
                self.services_element()
                
        elif self.token.type == 'INDENTATION':
            self.take_token('INDENTATION')
            self.skip_prod()
            self.top_level_element()
            self.services_element()
 
        
         
            