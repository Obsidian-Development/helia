package helia.extensions

import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingCoalescingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.member
import com.kotlindiscord.kord.extensions.commands.converters.impl.user
import com.kotlindiscord.kord.extensions.commands.parser.Arguments
import com.kotlindiscord.kord.extensions.commands.slash.AutoAckType
import com.kotlindiscord.kord.extensions.extensions.Extension
import com.kotlindiscord.kord.extensions.utils.respond
import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.ButtonStyle
import dev.kord.core.behavior.edit
import dev.kord.core.behavior.ban
import dev.kord.rest.builder.message.create.embed


import helia.TEST_SERVER_ID

import org.codehaus.groovy.ast.expr.Expression
import javax.script.ScriptEngineManager

@OptIn(KordPreview::class)
class CalculatorCommandH : Extension()   {
    override val name = "calculator"
    override suspend fun setup() {
        command() {
            name = "calculator"
            description = "Calculator command"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@CalculatorCommandH.kord
                val e = ScriptEngineManager().getEngineByName("js")
                var expression = ""


                message.respond {
                    embed {
                        title = "Calculator"
                        description = "this description value cannot be edited? "
                        components() {
                            interactiveButton {
                                label = "1"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "1"
                                    respond("```${expression}```")

                                }
                            }
                            interactiveButton {
                                label = "2"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "2"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "3"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "3"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "*"
                                style = ButtonStyle.Danger

                                action { // Easy button actions
                                    expression += "*"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "EXIT"
                                style = ButtonStyle.Success

                                action { // Easy button actions
                                    respond("If embeds were editable this would remove it")
                                }
                            }
                            interactiveButton {
                                label = "4"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "4"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "5"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "5"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "6"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "6"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "÷"
                                style = ButtonStyle.Danger

                                action { // Easy button actions
                                    expression += "/"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "←"
                                style = ButtonStyle.Success

                                action { // Easy button actions
                                    respond("Button ten pressed!")
                                }
                            }
                            interactiveButton {
                                label = "7"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "7"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "8"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "8"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "9"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "9"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "+"
                                style = ButtonStyle.Danger

                                action { // Easy button actions
                                    expression += "+"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "Clear"
                                style = ButtonStyle.Success

                                action { // Easy button actions
                                    expression = ""
                                    respond("Cleared the expression")
                                }
                            }
                            interactiveButton {
                                label = "00"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "00"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "0"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "0"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "."
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "."
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "-"
                                style = ButtonStyle.Danger

                                action { // Easy button actions
                                    expression += "-"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "="
                                style = ButtonStyle.Success

                                action { // Easy button actions
                                    var result = e.eval(expression)
                                    var formatedres = result.toString()
                                    expression = formatedres
                                    respond("```${formatedres}```")


                                }
                            }
                            interactiveButton {
                                label = "("
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += "("
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = ")"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    expression += ")"
                                    respond("```${expression}```")
                                }
                            }
                            interactiveButton {
                                label = "π"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    respond("Button  pressed!")
                                }
                            }
                        }


                    }
                }

            }
        }

        slashCommand() {
            name = "calculator"
            description = "Calculator command"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //invite(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@CalculatorCommandH.kord
                val e = ScriptEngineManager().getEngineByName("js")
                var expression = ""




                publicFollowUp {
                    var thisemb = embed {
                        title = "Calculator"
                        description = "this description value cannot be edited? "

                    }
                    components() {
                        interactiveButton {
                            label = "1"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "1"
                                respond("```${expression}```")

                            }
                        }
                        interactiveButton {
                            label = "2"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "2"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "3"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "3"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "*"
                            style = ButtonStyle.Danger

                            action { // Easy button actions
                                expression += "*"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "EXIT"
                            style = ButtonStyle.Success

                            action { // Easy button actions
                                respond("If embeds were editable this would remove it")
                            }
                        }
                        interactiveButton {
                            label = "4"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "4"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "5"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "5"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "6"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "6"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "÷"
                            style = ButtonStyle.Danger

                            action { // Easy button actions
                                expression += "/"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "←"
                            style = ButtonStyle.Success

                            action { // Easy button actions
                                respond("Button ten pressed!")
                            }
                        }
                        interactiveButton {
                            label = "7"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "7"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "8"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "8"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "9"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "9"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "+"
                            style = ButtonStyle.Danger

                            action { // Easy button actions
                                expression += "+"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "Clear"
                            style = ButtonStyle.Success

                            action { // Easy button actions
                                expression = ""
                                respond("Cleared the expression")
                            }
                        }
                        interactiveButton {
                            label = "00"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "00"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "0"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "0"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "."
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "."
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "-"
                            style = ButtonStyle.Danger

                            action { // Easy button actions
                                expression += "-"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "="
                            style = ButtonStyle.Success

                            action { // Easy button actions
                                var result = e.eval(expression)
                                var formatedres = result.toString()
                                expression = formatedres
                                respond("```${formatedres}```")


                            }
                        }
                        interactiveButton {
                            label = "("
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += "("
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = ")"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                expression += ")"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "π"
                            style = ButtonStyle.Secondary

                            action { // Easy button actions
                                respond("Button  pressed!")
                            }
                        }
                    }
                }

            }
        }
    }
}