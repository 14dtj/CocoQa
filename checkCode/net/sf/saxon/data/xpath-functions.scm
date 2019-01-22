<?xml version="1.0" encoding="UTF-8"?>
<scm:schema xmlns:scm="http://ns.saxonica.com/schema-component-model"
            generatedAt="2016-11-28T14:28:11.218Z"
            xsdVersion="1.0">
   <scm:complexType id="C0"
                    name="mapWithinMapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="C1"
                    derivationMethod="extension"
                    abstract="false"
                    variety="element-only">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
      <scm:attributeWildcard ref="C4"/>
      <scm:modelGroupParticle minOccurs="0" maxOccurs="unbounded">
         <scm:choice>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C5"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C6"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C7"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C8"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C9"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C10"/>
         </scm:choice>
      </scm:modelGroupParticle>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C5" to="1"/>
            <scm:edge term="C7" to="1"/>
            <scm:edge term="C10" to="1"/>
            <scm:edge term="C8" to="1"/>
            <scm:edge term="C6" to="1"/>
            <scm:edge term="C9" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C5" to="1"/>
            <scm:edge term="C7" to="1"/>
            <scm:edge term="C10" to="1"/>
            <scm:edge term="C8" to="1"/>
            <scm:edge term="C6" to="1"/>
            <scm:edge term="C9" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C11"
                    name="analyze-string-result-type"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="mixed">
      <scm:modelGroupParticle minOccurs="0" maxOccurs="unbounded">
         <scm:choice>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C12"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C13"/>
         </scm:choice>
      </scm:modelGroupParticle>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C12" to="1"/>
            <scm:edge term="C13" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C12" to="1"/>
            <scm:edge term="C13" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C14"
                    name="nullType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="empty">
      <scm:attributeWildcard ref="C15"/>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true"/>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C16"
                    name="group-type"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="mixed">
      <scm:attributeUse required="false" inheritable="false" ref="C17"/>
      <scm:elementParticle minOccurs="0" maxOccurs="unbounded" ref="C18"/>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C18" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C18" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C19"
                    name="booleanType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#boolean"
                    derivationMethod="extension"
                    abstract="false"
                    variety="simple"
                    simpleType="#boolean">
      <scm:attributeWildcard ref="C20"/>
   </scm:complexType>
   <scm:complexType id="C21"
                    name="arrayType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="element-only">
      <scm:attributeWildcard ref="C22"/>
      <scm:modelGroupParticle minOccurs="0" maxOccurs="unbounded">
         <scm:choice>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C23"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C24"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C25"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C26"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C27"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C28"/>
         </scm:choice>
      </scm:modelGroupParticle>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C28" to="1"/>
            <scm:edge term="C26" to="1"/>
            <scm:edge term="C27" to="1"/>
            <scm:edge term="C24" to="1"/>
            <scm:edge term="C23" to="1"/>
            <scm:edge term="C25" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C28" to="1"/>
            <scm:edge term="C26" to="1"/>
            <scm:edge term="C27" to="1"/>
            <scm:edge term="C24" to="1"/>
            <scm:edge term="C23" to="1"/>
            <scm:edge term="C25" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C29"
                    name="stringType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#string"
                    derivationMethod="extension"
                    abstract="false"
                    variety="simple"
                    simpleType="#string">
      <scm:attributeUse required="false" inheritable="false" ref="C30" default="false"/>
      <scm:attributeWildcard ref="C31"/>
   </scm:complexType>
   <scm:complexType id="C32"
                    name="numberWithinMapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="C33"
                    derivationMethod="extension"
                    abstract="false"
                    variety="simple"
                    simpleType="C34">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
      <scm:attributeWildcard ref="C35"/>
   </scm:complexType>
   <scm:complexType id="C36"
                    name="arrayWithinMapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="C21"
                    derivationMethod="extension"
                    abstract="false"
                    variety="element-only">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
      <scm:attributeWildcard ref="C22"/>
      <scm:modelGroupParticle minOccurs="0" maxOccurs="unbounded">
         <scm:choice>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C23"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C24"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C25"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C26"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C27"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C28"/>
         </scm:choice>
      </scm:modelGroupParticle>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C28" to="1"/>
            <scm:edge term="C26" to="1"/>
            <scm:edge term="C27" to="1"/>
            <scm:edge term="C24" to="1"/>
            <scm:edge term="C23" to="1"/>
            <scm:edge term="C25" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C28" to="1"/>
            <scm:edge term="C26" to="1"/>
            <scm:edge term="C27" to="1"/>
            <scm:edge term="C24" to="1"/>
            <scm:edge term="C23" to="1"/>
            <scm:edge term="C25" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:simpleType id="C34"
                   name="finiteNumberType"
                   targetNamespace="http://www.w3.org/2005/xpath-functions"
                   base="#double"
                   variety="atomic"
                   primitiveType="#double">
      <scm:minExclusive value="-INF"/>
      <scm:maxExclusive value="INF"/>
   </scm:simpleType>
   <scm:complexType id="C37"
                    name="stringWithinMapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="C29"
                    derivationMethod="extension"
                    abstract="false"
                    variety="simple"
                    simpleType="#string">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
      <scm:attributeUse required="false" inheritable="false" ref="C30" default="false"/>
      <scm:attributeWildcard ref="C31"/>
   </scm:complexType>
   <scm:complexType id="C38"
                    name="booleanWithinMapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="C19"
                    derivationMethod="extension"
                    abstract="false"
                    variety="simple"
                    simpleType="#boolean">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
      <scm:attributeWildcard ref="C20"/>
   </scm:complexType>
   <scm:complexType id="C33"
                    name="numberType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="C34"
                    derivationMethod="extension"
                    abstract="false"
                    variety="simple"
                    simpleType="C34">
      <scm:attributeWildcard ref="C35"/>
   </scm:complexType>
   <scm:complexType id="C1"
                    name="mapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="element-only">
      <scm:attributeWildcard ref="C4"/>
      <scm:modelGroupParticle minOccurs="0" maxOccurs="unbounded">
         <scm:choice>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C5"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C6"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C7"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C8"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C9"/>
            <scm:elementParticle minOccurs="1" maxOccurs="1" ref="C10"/>
         </scm:choice>
      </scm:modelGroupParticle>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C5" to="1"/>
            <scm:edge term="C7" to="1"/>
            <scm:edge term="C10" to="1"/>
            <scm:edge term="C8" to="1"/>
            <scm:edge term="C6" to="1"/>
            <scm:edge term="C9" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C5" to="1"/>
            <scm:edge term="C7" to="1"/>
            <scm:edge term="C10" to="1"/>
            <scm:edge term="C8" to="1"/>
            <scm:edge term="C6" to="1"/>
            <scm:edge term="C9" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C39"
                    name="nullWithinMapType"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="empty">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true"/>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:complexType id="C40"
                    name="match-type"
                    targetNamespace="http://www.w3.org/2005/xpath-functions"
                    base="#anyType"
                    derivationMethod="restriction"
                    abstract="false"
                    variety="mixed">
      <scm:elementParticle minOccurs="0" maxOccurs="unbounded" ref="C18"/>
      <scm:finiteStateMachine initialState="0">
         <scm:state nr="0" final="true">
            <scm:edge term="C18" to="1"/>
         </scm:state>
         <scm:state nr="1" final="true">
            <scm:edge term="C18" to="1"/>
         </scm:state>
      </scm:finiteStateMachine>
   </scm:complexType>
   <scm:element id="C25"
                name="string"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C29"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C12"
                name="match"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C40"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C23"
                name="map"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C1"
                global="true"
                nillable="false"
                abstract="false">
      <scm:identityConstraint ref="C41"/>
   </scm:element>
   <scm:element id="C18"
                name="group"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C16"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C27"
                name="boolean"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C19"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C42"
                name="analyze-string-result"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C11"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C28"
                name="null"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C14"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C26"
                name="number"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C33"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C24"
                name="array"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C21"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:element id="C13"
                name="non-match"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="#string"
                global="true"
                nillable="false"
                abstract="false"/>
   <scm:attributeGroup id="C43"
                       name="key-group"
                       targetNamespace="http://www.w3.org/2005/xpath-functions">
      <scm:attributeUse required="false" inheritable="false" ref="C2"/>
      <scm:attributeUse required="false" inheritable="false" ref="C3" default="false"/>
   </scm:attributeGroup>
   <scm:element id="C8"
                name="number"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C32"
                global="false"
                containingComplexType="C1"
                nillable="false"
                abstract="false"/>
   <scm:wildcard id="C22"
                 processContents="skip"
                 constraint="not"
                 namespaces="##local http://www.w3.org/2005/xpath-functions"/>
   <scm:wildcard id="C15"
                 processContents="skip"
                 constraint="not"
                 namespaces="##local http://www.w3.org/2005/xpath-functions"/>
   <scm:attribute id="C30"
                  name="escaped"
                  type="#boolean"
                  global="false"
                  inheritable="false"
                  containingComplexType="C29"/>
   <scm:element id="C9"
                name="boolean"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C38"
                global="false"
                containingComplexType="C1"
                nillable="false"
                abstract="false"/>
   <scm:element id="C6"
                name="array"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C36"
                global="false"
                containingComplexType="C1"
                nillable="false"
                abstract="false"/>
   <scm:element id="C7"
                name="string"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C37"
                global="false"
                containingComplexType="C1"
                nillable="false"
                abstract="false"/>
   <scm:wildcard id="C35"
                 processContents="skip"
                 constraint="not"
                 namespaces="##local http://www.w3.org/2005/xpath-functions"/>
   <scm:wildcard id="C4"
                 processContents="skip"
                 constraint="not"
                 namespaces="##local http://www.w3.org/2005/xpath-functions"/>
   <scm:unique id="C41"
               name="unique-key"
               targetNamespace="http://www.w3.org/2005/xpath-functions">
      <scm:selector xmlns:xs="http://www.w3.org/2001/XMLSchema"
                    xmlns:j="http://www.w3.org/2005/xpath-functions"
                    xpath="*"
                    defaultNamespace=""/>
      <scm:field xmlns:xs="http://www.w3.org/2001/XMLSchema"
                 xmlns:j="http://www.w3.org/2005/xpath-functions"
                 xpath="@key"
                 defaultNamespace=""/>
   </scm:unique>
   <scm:attribute id="C3"
                  name="escaped-key"
                  type="#boolean"
                  global="false"
                  inheritable="false"/>
   <scm:wildcard id="C20"
                 processContents="skip"
                 constraint="not"
                 namespaces="##local http://www.w3.org/2005/xpath-functions"/>
   <scm:element id="C10"
                name="null"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C39"
                global="false"
                containingComplexType="C1"
                nillable="false"
                abstract="false"/>
   <scm:element id="C5"
                name="map"
                targetNamespace="http://www.w3.org/2005/xpath-functions"
                type="C0"
                global="false"
                containingComplexType="C1"
                nillable="false"
                abstract="false">
      <scm:identityConstraint ref="C44"/>
   </scm:element>
   <scm:unique id="C44"
               name="unique-key-2"
               targetNamespace="http://www.w3.org/2005/xpath-functions">
      <scm:selector xmlns:xs="http://www.w3.org/2001/XMLSchema"
                    xmlns:j="http://www.w3.org/2005/xpath-functions"
                    xpath="*"
                    defaultNamespace=""/>
      <scm:field xmlns:xs="http://www.w3.org/2001/XMLSchema"
                 xmlns:j="http://www.w3.org/2005/xpath-functions"
                 xpath="@key"
                 defaultNamespace=""/>
   </scm:unique>
   <scm:wildcard id="C31"
                 processContents="skip"
                 constraint="not"
                 namespaces="##local http://www.w3.org/2005/xpath-functions"/>
   <scm:attribute id="C17"
                  name="nr"
                  type="#positiveInteger"
                  global="false"
                  inheritable="false"
                  containingComplexType="C16"/>
   <scm:attribute id="C2"
                  name="key"
                  type="#string"
                  global="false"
                  inheritable="false"/>
</scm:schema>
<?Σ 5a49b8d2?>
