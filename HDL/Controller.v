`timescale 1ns / 1ps


module Controller(
input [31:0]INSTR,
input  Equal,Zero,CO,OVF,less_than,
output reg PCSrc,Branch_control,
output reg [2:0]ImmSrc,
output reg memory_selection,
output reg [3:0] ALUControl,
output reg WD3Control,
output reg SrcAcontrol, ALUSrc, RegWrite, MemtoReg,
output reg [1:0] shamt_control,shifter_control,MemWrite,
output [2:0] funct3,
output [6:0]  op,
output funct7
    );
reg [2:0] deneme;
assign funct3 =INSTR[14:12];
assign funct7_5 =INSTR[31];
assign op =INSTR[6:0];
assign cond=INSTR[6:2];

//assign branch_cond=(INSTR[6:2]==11000)? INSTR[14:12]:3'b010 ;//I give 010 since there is no 
//branch instruction having 010.PCSrc will be 0==>PC+4
always@(*)begin 
    case(op)
        7'b0000011:begin //LOAD inst. (LOAD)(lw,lb,lbu,lh,lhu)
        ImmSrc=3'b000;  //For I
        //memory_selection=INSTR[13:12];//For memory selections 10-word,01-Half-word,00-byte.
        WD3Control=1'b0;
        ALUControl=4'b1011;//ADD normal
        SrcAcontrol=1'b0;//RD1
        ALUSrc=1'b1;//immediate
        shamt_control=2'b00;//shmat=0
        shifter_control=2'b00;//does not matter
        PCSrc=1'b0;
        RegWrite=1'b1;//x[rd]=
        MemtoReg=1'b1;
        MemWrite=2'b11;
        Branch_control=1'b0;
        end
        
        7'b0110011:begin //R inst.(Arithmatic),(AND,ADD,SUB,XOR,OR)
        ImmSrc=3'b000;
        WD3Control=1'b0;
        SrcAcontrol=1'b0;//RD1
        ALUSrc=1'b0;//RD2 immediate
        shamt_control=2'b00;//shmat=0
        shifter_control=2'b00;//does not matter
        PCSrc=1'b0;//pc+4
        RegWrite=1'b1;//x[rd]=
        MemtoReg=1'b0;
        MemWrite=2'b11;
        Branch_control=1'b0;

        case(funct3)
            3'b111:ALUControl=4'b0000;//AND
            3'b000:ALUControl=((INSTR[31:27]==5'b00000)? 4'b1011 :4'b1100);//ADD for 00000,SUB for 01000
            3'b100:ALUControl=4'b0101;//XOR
            3'b110:ALUControl=4'b0001;//OR
            3'b101:begin 
            ALUControl=4'b1110;//MOV RD1
            shifter_control=(INSTR[30])?2'b10:2'b01;
            shamt_control=2'b01;
            
            end
            3'b001:begin
            ALUControl=4'b1110;             //MOV RD1
            shifter_control=2'b00;
            shamt_control=2'b01;
            end
            3'b010:ALUControl=4'b0100;
            3'b011:ALUControl=4'b0110;
        endcase
        end
        
        7'b0010011:begin //Immediate inst.(Immediate Arithmatic),(ADDİ,ANDİ,XORİ,ORİ)
        ImmSrc=3'b000;              //For I
        WD3Control=1'b0;
        SrcAcontrol=1'b0;           //RD1
        ALUSrc=1'b1;                //immediate
        shamt_control=2'b00;        //shmat=0
        shifter_control=2'b00;      //does not matter
        PCSrc=1'b0;
        RegWrite=1'b1;              //x[rd]=
        MemtoReg=1'b0;
        MemWrite=2'b11;
        deneme=funct3;
        Branch_control=1'b0;

        case(funct3)
            3'b111:ALUControl=4'b0000;          //ANDi
            3'b000:ALUControl=4'b1011;          //Addi
            3'b100:ALUControl=4'b0101;          //XORi
            3'b110: ALUControl=4'b0001;         //ORi
            3'b101:begin 
            ALUControl=4'b1110;//MOV RD1
            shifter_control=(INSTR[30])?2'b10:2'b01;
            shamt_control=2'b10;
            end
            3'b001:begin
            ALUControl=4'b1110;             //MOV RD1
            shifter_control=2'b00;
            shamt_control=2'b10;
            end
            3'b010:ALUControl=4'b0100;
            3'b011:ALUControl=4'b0110;

            default:ALUControl=4'b1011;     //ADD for default
        endcase
        end
        
        7'b1100111:begin //Immediate inst.(JALR)
        WD3Control=1'b1;                //pc+4 to x[rd]
        ImmSrc=3'b000;                  //For I
        ALUControl=4'b1011;             //ADD 
        SrcAcontrol=1'b0;                //RD1
        ALUSrc=1'b1;                    //immediate
        shamt_control=2'b00;            //shmat=0
        shifter_control=2'b00;          //does not matter
        PCSrc=1'b1;
        RegWrite=1'b1;                  //x[rd]=pc+4
        MemtoReg=1'b0;
        MemWrite=2'b11;
        Branch_control=1'b0;

        end
        
        7'b1100011:begin                //Branch inst.(blt,bltu,bge,bgeu,bne,beq)
        ImmSrc=3'b001;  
        WD3Control=1'b0;
        SrcAcontrol=1'b0;               //RD1
        ALUSrc=1'b0;//RD2
        shamt_control=2'b00;//shmat=0
        shifter_control=2'b00;//does not matter
        PCSrc=1'b0;
        RegWrite=1'b0;              // no x[rd]=
        MemtoReg=1'b0;
        MemWrite=2'b11;
        case(INSTR[14:13])
            2'b10:begin             //blt and bge
            ALUControl=4'b1000;
            Branch_control=(INSTR[12])?(less_than)?1'b0:1'b1:(less_than)?1'b1:1'b0;
            end
            2'b00:begin              //bge and bne
            ALUControl=4'b1001;
            Branch_control=(INSTR[12])?(Equal)?1'b0:1'b1:(Equal)?1'b1:1'b0;
            end
            2'b11:begin 
            ALUControl=4'b0111;
            Branch_control=(INSTR[12])?(less_than)?1'b0:1'b1:(less_than)?1'b1:1'b0;
            end
        endcase       
        end
        
        7'b0100011:begin// Store inst.(sw,sb,sbu,sh,shu)
        ImmSrc=3'b010;  //For S
        MemWrite=INSTR[13:12];          //For memory selections 10-word,01-Half-word,00-byte.
        WD3Control=1'b0;
        ALUControl=4'b1011;             //ADD 
        SrcAcontrol=1'b0;               //RD1
        ALUSrc=1'b1;                    //immediate
        shamt_control=2'b00;            //shmat=0
        shifter_control=2'b00;          //does not matter
        PCSrc=1'b0;
        RegWrite=1'b0;                  // no x[rd]=
        MemtoReg=1'b0;
        Branch_control=1'b0;

        end
        
        7'b1101111:begin //Jump inst. (JAL)
        ImmSrc=3'b011;  
        WD3Control=1'b1;        //Since in this instr. x[rd]=pc+4
        ALUControl=4'b1011;     //ADD
        SrcAcontrol=1'b1;       //pc
        ALUSrc=1'b1;            //immediate
        shamt_control=2'b00;    //shmat=0
        shifter_control=2'b00;  //does not matter
        PCSrc=1'b0;
        RegWrite=1'b1;          //x[rd]=
        MemtoReg=1'b0;
        MemWrite=2'b11;
        Branch_control=1'b1;

        end
        
        7'b0110111:begin //U inst. (LUI) x[rd]=sext(imm[31:12]<<12)
        ImmSrc=3'b100;
        ALUControl=4'b1101;         //MOV in ALU
        WD3Control=1'b0;            //Since in this instr. x[rd]=pc+4
        SrcAcontrol=1'b1;           //pc //no change
        ALUSrc=1'b1;                //RD2
        shamt_control=2'b00;        //shmat=0
        shifter_control=2'b00;      //does not matter
        PCSrc=1'b0;
        RegWrite=1'b1;              //x[rd]=
        MemtoReg=1'b0;
        MemWrite=2'b11;
        Branch_control=1'b0;


        end
        7'b0010111:begin //U inst. (AUIPC) x[rd]=pc+sext(imm[31:12]<<12)
        SrcAcontrol=1'b1;       //PC as SrcA
        ALUSrc=1'b1;            //Imm 
        ImmSrc=3'b100;
        ALUControl=4'b1011;     //MOV in ALU
        WD3Control=1'b0;        //Since in this instr. x[rd]=pc+4
        shamt_control=2'b00;    //shmat=0
        shifter_control=2'b00;  //does not matter
        PCSrc=1'b0;
        RegWrite=1'b1;//x[rd]=
        MemtoReg=1'b0;
        MemWrite=2'b11;
        Branch_control=1'b0;

        end
        
       
        default:begin  ImmSrc=3'b000;
         memory_selection=2'b10;//Word in memory
        end
    endcase
//memory selection will be given to the shifters not to the memory unit.
//assign PCSrc=(branch_cond==000&Z)|(branch_cond==001&~Z)|(branch_cond==100&less_than)|(branch_cond==110&less_than)|(branch_cond==101&greater_than)|(branch_cond==111&greater_than)|~(branch_cond==010);
end
endmodule
